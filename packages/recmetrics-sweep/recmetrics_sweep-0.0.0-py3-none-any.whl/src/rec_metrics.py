from functional import *
from tabulate import tabulate

# Class for conveniently executing, storing, and loading evaluation of recommendations.
# Can be done in batches.
class RecMetrics:
  # Metrics are case sensitive. Note that specifying k overrides k_vals.
  def __init__(self, metrics=['k', 'MRR', 'NDCG', 'Precision', 'Recall', 'F', 'Coverage', '#Coverage', 'PCoverage', '#PCoverage'],
          k_vals=[5], k=None, verbose=False):
    self.metrics = metrics
    self.metrics_indices = {}
    self.num_metrics = len(self.metrics)
    metric_i = 0
    for metric in self.metrics:
      self.metrics_indices[metric] = metric_i
      metric_i += 1
    if k:
      k_vals = k
    if not hasattr(k_vals, '__iter__'):
      k_vals = [k_vals]
    self.k_vals = k_vals
    self.scores = []
    for k in k_vals:
      k_scores = []
      for metric in self.metrics:
        if metric == 'k':
          k_scores.append(k)
        elif metric.startswith('#'):
          k_scores.append(0)
        elif 'Coverage' in metric:
          if metric.startswith('P'):
            k_scores.append(set())
          else:
            k_scores.append(set())
        else:
          k_scores.append([])
      self.scores.append(k_scores)
    self.norms = []
    self.num_samples = 0
    self.num_items = 0
    self.verbose = verbose
    if self.verbose:
       vprint(metrics, 'Initialized RecMetrics with metrics')
       vprint(self.k_vals)
  
  def restart(self, metrics=[]):
    if len(metrics):
      for metric in metrics:
        for trial_i in range(self.num_metrics):
          if 'Coverage' not in metric:
            self.scores[trial_i][self.metrics_indices[metric]] = []
          else:
            self.scores[trial_i][self.metrics_indices[metric]] = set()
          self.norms[trial_i][self.metrics_indices[metric]] = 0
  
  def score(self, true_indices, true_weights, pred_relevances, verbose=None):
    if not verbose:
      verbose = self.verbose
    self.num_items = vwid(pred_relevances)
    calced_scores, metrics = score_rec_metrics(true_indices, true_weights, 
              pred_relevances, metrics=self.metrics, 
              metrics_indices=self.metrics_indices, k_vals=self.k_vals, verbose=verbose)
    if vlen(self.k_vals) == 1:
      calced_scores = [calced_scores]
    for k_i in range(len(self.k_vals)):
      for metric_i in range(self.num_metrics):
        metric_scores = calced_scores[k_i][metric_i]
        metric = self.metrics[metric_i]
        if self.verbose:
          if metric == 'Coverage':
            lprint(metric_scores, metric)
          else:
            aprint(metric_scores, metric)
        if 'k' == metric:
          continue
        elif metric.startswith('#'): # Number of items (e.g. for #Coverage)
          # This depends on the respective coverage being updated first
          num_covered = vlen(self.scores[k_i][self.metrics_indices[metric.replace('#', '')]])
          self.scores[k_i][metric_i] = num_covered
        elif 'Coverage' not in metric:
          self.scores[k_i][metric_i].extend(metric_scores)
        else:
          self.scores[k_i][metric_i].update(metric_scores)
    self.num_samples += vlen(true_indices)
    if self.verbose:
      vprint(self.num_samples, 'Samples scored')
    return self.scores
  
  def normalize(self):
    self.norms = []
    for k_i in range(vlen(self.scores)):
      self.norms.append(norm_rec_metrics(self.scores[k_i], self.metrics, self.num_items))
    if self.verbose:
      vprint(self.norms, 'Normalized scores')
  
  def print(self, metrics=None):
    if not vlen(self.norms):
      self.normalize()
    if not metrics:
      metrics = self.metrics
      norms = self.norms
    else:
      norms = []
      for metric in metrics:
        norm.append(self.norms[self.metrics_indices[metric]])
    print_rec_metrics(norms, metrics)
    
  def plot(self, metrics=None):
    if not vlen(self.norms):
      self.normalize()
    if not metrics:
      metrics = self.metrics
      norms = self.norms
    else:
      norms = []
      for metric in metrics:
        norm.append(self.norms[self.metrics_indices[metric]])
    plot_rec_metrics(norms, metrics)
  
  def compare(self, methods):
    compare_methods([self].extend(methods))
  
  def save(self, filename):
    with open(filename, 'wb') as file:
      pickle.dump(self, file)
  
  def load(self, filename):
    with open(filename, 'rb') as file:
      self = pickle.load(file)
  
  def save_norms(self, filename, delim=','):
    with open(filename, 'w') as file:
      norms_writer = csv.writer(file, delimiter=delim, quotechar="'")
      norms_writer.writerow(self.metrics)
      norms_writer.writerows(self.norms)
      if self.verbose:
        vprint(filename, 'Saved normalized scores as csv')
  
  def load_norms(self, filename, delim=','):
    self.norms = []
    with open(filename, 'r') as file:
      norms_reader = csv.reader(file, delimiter=delim, quotechar="'")
      self.metrics = next(norms_reader)
      for row in norms_reader:
        self.norms.append(row)
    return self.norms

  def call(self, *argv, print_metrics=True, plot_k=False, **kwargs):
    return self.__call__(*argv, print_metrics=True, plot_k=False, **kwargs)
  
  def __call__(self, *argv, print_metrics=True, plot_k=False, **kwargs):
    self.score(*argv, **kwargs)
    self.normalize()
    if print_metrics:
      self.print()
    if plot_k:
      self.plot()
    return self.norms
  
  def __str__(self):
    return "\n"+tabulate(self.norms, headers=self.metrics)+"\nSamples: "+str(self.num_samples)
#     return str(self.metrics)+"\n\tk:"+str(self.k_vals)+"\n\tnormalized scores:"+str(self.norms)+"\n\tSamples: "+str(self.num_samples)
  
  def copy(self):
    return self.__copy__()
  
  def __copy__(self):
    obj = type(self).__new__(self.__class__)
    obj.__dict__.update(self.__dict__)
    return obj
  

