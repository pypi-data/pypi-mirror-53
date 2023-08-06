
import sys
import pickle
import csv
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from math import log10, floor


# Round value to sig_digits significant digits.
def round_sig(x, sig=3):
  if x == 0:
    return 0
  return round(x, sig-int(floor(log10(abs(x))))-1)

# Normalize the formatting of scores.
def format_score(score, sig_digits=3, use_scientific=False):
  score = to_num(score)
  if score == False:
    try:
      score = float(score)
    except ValueError:
      pass
  if score == 0:
    return "0"
  if sig_digits is not None:
    score = round_sig(score, sig=sig_digits)
  if score < 1:
    if use_scientific:
      score = '{:.{}E}'.format(float(score),sig_digits-1)
#     else:
#       if not isinstance(score, int):
#         score = '%f' % score
  return score

# Pad matrix with following zeros.
def lists_to_matrix(lists, dtype=float):
  lens = [len(entries) for entries in lists]
  maxlen=max(lens)
  matrix = np.zeros((len(lists),maxlen), dtype)
  pad_mask = np.arange(maxlen) < np.array(lens)[:,None]
  matrix[pad_mask] = np.concatenate(lists)
  return matrix

# Pad each row with a value that is different for each row
def row_val_pad(vector, pad_width, iaxis, kwargs):
  if iaxis == 1:
    vals = kwargs['vals']
    row_i = kwargs.get('row_i', 0)
    pad_value = vals[row_i]
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    if not row_i:
      kwargs['row_i'] = 1
    else:
      kwargs['row_i'] += 1
  return vector

# Pad indices matrix with zeros and pad weights matrix with
# the value in weights for index 0 (if there is one; else 0).
def indices_values_matrices(indices_lists, weights_lists, lens=None):
  if not lens:
    lens = np.array([vlen(entries) for entries in indices_lists])
  maxlen=np.max(lens)
  num_rows = vlen(indices_lists)
  indices_matrix = np.zeros((num_rows,maxlen), int)
  weights_matrix = np.zeros((num_rows,maxlen), float)
  originals_mask = np.arange(maxlen) < lens[:,None]
  indices_matrix[originals_mask] = np.concatenate(indices_lists)
  weights_matrix[originals_mask] = np.concatenate(weights_lists)
  zero_vals = []
  for row_i in range(num_rows):
    try:
      zero_i = indices_lists[row_i].index(0)
      zero_val = weights_lists[row_i][zero_i]
    except ValueError:
      zero_val = 0
    zero_vals.append(zero_val)
  zero_vals = np.asarray(zero_vals)
  pad_lens = maxlen-lens
  zero_vals = np.repeat(zero_vals, maxlen-lens)
  zeros_mask = np.arange(maxlen) >= lens[:,None]
  weights_matrix[zeros_mask] = zero_vals
#   weights_matrix = np.pad(weights_matrix, ((0, 0), (0, maxlen)), row_val_pad, vals=zero_vals)
  
  return indices_matrix, weights_matrix

# DCG = sum of ((2^relevance score - 1) / log2(rank + 1)) for rank=(1 to k)
def dcg(pred_scores, k=5):
  discounts = np.log2(np.arange(0, k) + 2) # 2, 3, ... k+1
  if k > len(pred_scores[0]):
    pred_scores = np.pad(pred_scores, ((0, 0), (0, k)), 'constant')
  divided = np.nan_to_num(np.divide(2**pred_scores[:, :k] - 1, discounts))
  return np.sum(divided, axis=1)


# For individual reciprocal rank
# Positive values are assumed to be correct or good recommendations
def find_first_correct(scores_row):
  try:
    return np.argwhere(scores_row > 0)[0][0] + 1 # Start rank at 1
  except IndexError:
    # Default to last rank possible if no correct recommendation is found.
    return len(scores_row)


# For Mean Reciprocal Rank
def find_first_corrects(scores_matrix):
  return np.apply_along_axis(find_first_correct, 1, scores_matrix)


# For Correct Coverage@k.
# What unique items (indices) were correctly recommended in the top k?
# Slice predicted indices beforehand for top k (predicted[:k])
def find_num_corrects(predicted, row_i=-1, relevances=[]):
  row_i += 1
  
  return np.where(relevances[row_i][predicted] > 0)


# Calculate and return MRR, NDCG@k, Precision@k, Recall@k, Coverage@k, Correct Coverage@k
# Scores are returned by row except for the two coverages, which are returned as sets of indices
  # (in case further analysis is desired).
def score_rec_metrics(true_indices, true_weights, pred_relevances, 
                      metrics=['k', 'MRR', 'NDCG', 'Precision', 'Recall', 
                               'F', 'Coverage', '#Coverage', 
                               'PCoverage', '#PCoverage'],
                     metrics_indices=None, k_vals=[5], k=None, verbose=False):
  if hasattr(pred_relevances, 'toarray'):
    pred_relevances = pred_relevances.toarray()
  if vlen(true_indices) != vlen(true_weights) or vlen(true_indices) != vlen(pred_relevances):
    eprint('true_indices, true_weights, and pred_relevances must have the same first dimension (samples)')
    lprint(true_indices)
    lprint(true_weights)
    lprint(pred_relevances)
    return

  start()
  if k:
    k_vals = k
  if not hasattr(k_vals, '__iter__'):
    k_vals = [k_vals]

  true_lens = None
  if isinstance(true_indices[0], list) or isinstance(true_weights[0], list):
    true_lens = [len(entries) for entries in true_indices] # This is faster with lists.
    true_indices, true_weights = indices_values_matrices(true_indices, true_weights)
  scores = []
  for k_i in range(len(k_vals)):
    scores.append([[] for i in range(len(metrics))])
  if not metrics_indices:
    metrics_indices = {}
    metric_i = -1
    for metric in metrics:
      metrics_indices[metric] = metric_i
      metric_i += 1
  if verbose:
    end("Setup")
  
  # Negate relevances to sort and distinguish from positive true_weights
  pred_relevances = pred_relevances * -1 
  # vprint(pred_relevances, 'negated pred relevances')
  # Sort indices corresponding to items
  max_k = max(k_vals)
  if 'MRR' in metrics_indices:
    pred_ordered = np.argsort(pred_relevances)
    if verbose:
      end("Sorting all")
  else:
    pred_ordered = np.argpartition(pred_relevances, max_k) # Sort only once for the highest k
    if verbose:
      end("Sorting top "+str(max_k))
  
  # Insert true weights to relevances matrix to score ordered indices
  np.put_along_axis(pred_relevances, true_indices, true_weights, axis=1)
  # vprint(pred_relevances, 'relevances with true weights')
  try:
    # Reward top indices that had a positive true weight inserted
    top_scores = np.take_along_axis(pred_relevances, pred_ordered, axis=1)
  except ValueError as e:
    eprint(e)
    aprint(pred_relevances)
    aprint(pred_ordered)
    
  if verbose:
    end("Score predictions")
  
  if 'MRR' in metrics_indices:
    # MRR = 1 / rank of first correct recommendation
    first_corrects = find_first_corrects(top_scores)
    mrr_scores = np.reciprocal(first_corrects.astype(float))
    mrr_i = metrics_indices['MRR']
    for k_i in range(len(k_vals)):
      scores[k_i][mrr_i] = mrr_scores
    if verbose:
      end("MRR")
  
  num_items = vwid(pred_relevances)
  for k_i in range(len(k_vals)):
    k = k_vals[k_i]
    if 'k' in metrics_indices:
      scores[k_i][metrics_indices['k']] = k
    # Don't let k be greater than the number of possible items to recommend.
    if verbose:
      vprint(k)
      vprint(num_items)
    if k > num_items:
      if verbose:
        print("k="+str(k)+" set to "+str(num_items)+" to match number of items")
      k = num_items
    
    top_k_scores = top_scores[:, :k]
    # Set predicted relevances to 0 so only the true weights remain
    np.clip(top_k_scores, a_min=0, a_max=None, out=top_k_scores)

  
    if 'Precision' in metrics_indices or 'Recall' in metrics_indices or 'F' in metrics_indices:
      # Get number of correct indices recommended
      num_corrects = np.count_nonzero(top_k_scores, axis=1)
      if 'Precision' in metrics_indices or 'F' in metrics_indices:
        # precision@k = number correct@k / k
        precision_k_scores = num_corrects * 1/k
        scores[k_i][metrics_indices['Precision']] = precision_k_scores
        if verbose:
          end("Count num_corrects and Precision")
    
   
      if 'Recall' in metrics_indices or 'F' in metrics_indices:
        # How many true/correct recommendations are there in total?
        if true_lens is None:
          true_lens = np.count_nonzero(pred_relevances, axis=1)
        # recall@k = number correct@k / total possible correct
        # nan to num just in case someone wants to allow samples where there are no true recommendations (divide by 0)
        recall_k_scores = np.nan_to_num(np.divide(num_corrects, true_lens))
        scores[k_i][metrics_indices['Recall']] = recall_k_scores
        if verbose:
          end("Recall")

    
      if 'F' in metrics_indices:
        # F@k = precision * recall / (precision + recall)
        precision_recall = np.nan_to_num(np.divide(precision_k_scores * recall_k_scores, precision_k_scores + recall_k_scores), copy=False)
        f_k_scores = 2 * precision_recall
        scores[k_i][metrics_indices['F']] = f_k_scores
        if verbose:
          end("F Score")

    if 'NDCG' in metrics_indices:
      # DCG = sum of ((2^relevance score - 1) / log2(rank + 1)) for rank=(1 to k)
      pred_dcg = dcg(top_k_scores, k)
      ideal_dcg = dcg(true_weights, k)
      # NDCG = predicted DCG / ideal DCG
      ndcg_scores = np.nan_to_num(np.divide(pred_dcg, ideal_dcg))
      scores[k_i][metrics_indices['NDCG']] = ndcg_scores
      if verbose:
        end("NDCG")

  if 'Coverage' in metrics_indices:
    for k_i in range(len(k_vals)):
      k = k_vals[k_i]
      # Add top k to coverage
      top_k_pred = pred_ordered[:, :k]
      covered = set(np.unique(top_k_pred))
      scores[k_i][metrics_indices['Coverage']] = covered
      if '#Coverage' in metrics_indices:
        scores[k_i][metrics_indices['#Coverage']] = vlen(covered)
      if verbose:
        end("Coverage@"+str(k))

  # Find Correct Coverage by finding indices of correct recommendations in each row.
  if 'PCoverage' in metrics_indices:
    # Do this after each k's Coverage to avoid making a copy.
    # Top k indices
    top_k_pred = pred_ordered[:, :max_k] # 
    top_k_pred[top_k_scores == 0] = -1

    for k_i in range(len(k_vals)):
      k = k_vals[k_i]
      top_k_pred = pred_ordered[:, :k]
      covered_correct = set(top_k_pred.flatten())
      covered_correct.discard(-1)
      scores[k_i][metrics_indices['PCoverage']] = covered_correct
      if '#PCoverage' in metrics_indices:
        scores[k_i][metrics_indices['#PCoverage']] = vlen(covered_correct)
      if verbose:
        end("PCoverage@"+str(k))
  if len(k_vals) == 1:
    scores = scores[0]
  return scores, metrics

# Given metrics by sample from score_rec_metrics, return normalized scores (usually the mean).
def norm_rec_metrics(scores, metrics, num_items=1):
  norms = []
  for metric_i in range(len(metrics)):
    metric = metrics[metric_i]
    if metric == 'k' or metric.startswith('#'):
      norm = scores[metric_i]
    elif 'Coverage' not in metric:
      norm = np.asarray(scores[metric_i]).mean()
    else:
      norm = vlen(scores[metric_i]) / num_items
    norms.append(norm)
  return norms

# Calculate and return normalized scores.
# Optional: Run metrics for different values of k (where k is iterable)
# Optional: Set plot_k=True to plot metrics by k values.
def rec_metrics(true_indices, true_weights, pred_relevances, covered=set(), covered_correct=set(), k=5, print_metrics=True, plot_k=False):
  k_metrics = []
  if not hasattr(k, '__iter__'):
    k_metrics.append(norm_rec_metrics(*score_rec_metrics(true_indices, true_weights, pred_relevances, k=k)))
  else:
    for k_trial in k:
      k_metrics.append([k_trial, *norm_rec_metrics(*score_rec_metrics(true_indices, true_weights, pred_relevances, k=k_trial))])
  # Print metrics in a table with k rows
  if print_metrics:
    print_rec_metrics(k_metrics)
  # Plot metrics by k
  if plot_k:
    plot_rec_metrics(k_metrics)
  if len(k_metrics) == 1:
    return k_metrics[0]
  return k_metrics


def print_rec_metrics(norms, metrics):
  print(tabulate(norms, headers=metrics))
  

def plot_rec_metrics(norms, metrics):
  import matplotlib.pyplot as plt
  k_metrics = np.array(k_metrics)
  fig, ax = plt.subplots()
  n_groups = len(k_metrics[0])-1
  index = np.arange(n_groups)
  bar_width = 0.35
  opacity = 0.4
  plt.plot(k, k_metrics[:, 1], 'r--', label='NDCG') # NDCG
  plt.plot(k, k_metrics[:, 2], label='Precision')

  plt.xlabel('k')
  plt.ylabel('Metric scores')
  plt.title('Recommender System Metrics by k')
  plt.grid(True)
  plt.show()

# Methods is a list of RecMetrics objects
# def compare_methods(methods):
  
  
