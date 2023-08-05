import numpy as np
import pandas as pd
from scipy import stats
import scipy.stats as stats
import matplotlib.pyplot as plt

def bootstrap(x, resamples=10000):
    """Draw bootstrap resamples from the array x.

    Parameters
    ----------
    x: np.array, shape (n, )
      The data to draw the bootstrap samples from.
    
    resamples: int
      The number of bootstrap samples to draw from x.
    
    Returns
    -------
    bootstrap_samples: List[np.array]
      The bootstrap resamples from x.  
      Each array is a single bootstrap sample.
    """
    n_obs = x.shape[0]
    boot_samples = []
    for k in range(resamples):
        boot_idxs = np.random.randint(n_obs, size=n_obs)
        boot_sample = x[boot_idxs]
        boot_samples.append(boot_sample)
    return boot_samples

class df_percentile():
  def __init__(self, df, col_names, col_to_separate):
    '''
    Instantiates the class using a dataframe, a list of the columns of interest, a column to separate the df into by percentile.

    Parameters
    ----------
    df - dataframe

    col_names = list of the columns of interests

    col_to_separate = column to separate DF by into two groups

    '''
    if col_to_separate not in df.columns:
      raise Exception(f"{col_to_separate} not in df") 
    for col_name in col_names:
      if col_name not in df.columns:
        raise Exception(f"{col_name} not in df") 
    self.df = df
    self.col_names = col_names
    self.col_to_separate = col_to_separate
    print(f"This dataframe is separated by {self.col_to_separate}")

  def __str__(self):
    '''
    Output when you print the class

    Returns
    ----------
    
    Str of the columns selected

    '''

    return f"This dataframe is separated by {self.col_to_separate}"

  def separate_df(self, percentile):
    '''
    Separates the df into two groups by a selected column and by percentile

    Parameters
    ----------
    percentile - int of percentile to split dataframe by


    Returns
    ----------
    Tuple of two dataframes, one dataframe of the upper bound group and one of the lower bound group.

    '''
    col = self.df[self.col_to_separate]
    cut_off = np.percentile(col, percentile)
    self.upper_bound, self.lower_bound = self.df[col >= cut_off], self.df[col < cut_off]
    return (self.upper_bound, self.lower_bound)

  def return_stats(self, percentile, col_name):
    '''
    Draw p-values and means of samples from dataframes and columns of interest separating dataframe entries by percentiles
    using student's t-test.

    Parameters
    ----------
    percentile - int of percentile to split dataframe by

    col_name - str of column name of interest 

    Returns
    -------
    Tuple of pvalue, mean of the column from the group in the upper bound, mean of the column from the group in the lower bound

    '''
    upper, lower = self.separate_df(percentile)
    column1, column2 = upper[f'{col_name}'], lower[f'{col_name}']
    t_stat, pvalue = stats.ttest_ind(column1, column2)
    return pvalue, column1.mean(), column2.mean()

  def create_df(self, percentile):
    '''
    Create a dataframe of pvalues, means of columns tested.

    Parameters
    ----------
    percentile - int of percentile to split dataframe by

    col_names - list of str of column names of interest 

    Returns
    -------
    Dataframe showing pvalues, means of the columns from the upper bound group, means of the columns from the lower bound group
    
    '''
    pvalues = []
    upper_means = []
    lower_means = []
    for col_name in self.col_names:
      pvalue, upper_mean, lower_mean = self.return_stats(percentile, col_name)
      pvalues.append(pvalue)
      upper_means.append(upper_mean)
      lower_means.append(lower_mean)
    d = {'p-values': pvalues, 'upper_bound_means': upper_means, 'lower_bound_means': lower_means}  
    df = pd.DataFrame(d, index=[self.col_names]) 
    return df

  def bootstrap(self, percentile, col_name, n_simulations=10000, ci = 95):
    '''
    Resamples from a dataframe by percentile on the column of interest per # of simulations.
    Create a histogram of the bootstrapped data.

    Parameters
    ----------
    percentile - int of percentile to split dataframes by

    col_name - column name of interest

    n_simulations - number of times to bootstrap, default to 10000

    Returns
    -------
    Histogram of the results with specified confidence interval, sample distribution means

    '''
    self.ci = ci
    upper, lower = self.separate_df(percentile)
    bs_upper, bs_lower = bootstrap(np.array(upper[col_name]), n_simulations), bootstrap(np.array(lower[col_name]), n_simulations)
    higher_bound_bs, lower_bound_bs = [sample.mean() for sample in bs_upper], [sample.mean() for sample in bs_lower]
    lower_bound = (100-self.ci)/2
    self.lower_ci_h, self.upper_ci_h = np.percentile(higher_bound_bs, [lower_bound, 100-lower_bound])
    self.lower_ci_l, self.upper_ci_l = np.percentile(lower_bound_bs, [lower_bound, 100-lower_bound])
    # self.lower_ci_h, self.upper_ci_h = np.percentile(higher_bound_bs, [2.5, 97.5])
    # self.lower_ci_l, self.upper_ci_l = np.percentile(lower_bound_bs, [2.5, 97.5])
    self.h_bs_mean = np.mean(higher_bound_bs)
    self.l_bs_mean = np.mean(lower_bound_bs)
    fig, ax = plt.subplots(figsize = (12,4))
    ax.hist(higher_bound_bs, alpha=0.5, bins=20, label='Higher Paid')
    ax.hist(lower_bound_bs, alpha=0.5, bins=20, label ='Lower Paid')
    ax.axvline(self.lower_ci_h, color='blue', linestyle="--", alpha=0.5, label=f'Higher Bound {self.ci}% CI')
    ax.axvline(self.upper_ci_h, color='blue', linestyle="--", alpha=0.5)
    ax.axvline(self.lower_ci_l, color='red', linestyle="--", alpha=0.5, label=f'Lower Bound {self.ci}% CI')
    ax.axvline(self.upper_ci_l, color='red', linestyle="--", alpha=0.5)
    ax.axvline(self.h_bs_mean, color='green', linestyle="--", alpha=0.5, label='Higher Bound Mean')
    ax.axvline(self.l_bs_mean, color='black', linestyle="--", alpha=0.5, label='Lower Bound Mean')
    ax.legend()
    ax.set_xlabel(f'{col_name} means')
    ax.set_ylabel('Count')
    ax.set_title(f'Bootstrapped {col_name} Sample Means Distribution')
    plt.show()
    plt.ion()

  def bootstrap_stats(self):
    '''
    Prints results from bootstrapped data for readability

    Returns
    -------
    Str of confidence interval bounds, sample distribution means

    '''
    return print(f'''
    The {self.ci}% confidence intervals for the upper bound ranges from {self.lower_ci_h} to {self.upper_ci_h}.
    The lower bound group ranges from {self.lower_ci_l} and {self.upper_ci_l}.
    Means of the distribution: 
    Higher Paid Group: {self.h_bs_mean}
    Lower Paid Group:{self.l_bs_mean}
     ''')

  def corr(self, percentile, col_name):
    '''
    Finds the pearson correlation coefficient of a given dataframe and column of interest separated by percentile.

    Parameters
    ----------
    percentile - int of percentile to separate df by

    col_name - str of column name of interest

    Returns
    -------
    Str of pearson correlation coefficients and their pvalues

    '''
    u, l = self.separate_df(percentile)
    l_corr, l_pvalue = stats.pearsonr(l[self.col_to_separate], l[col_name])
    u_corr, u_pvalue = stats.pearsonr(u[self.col_to_separate], u[col_name])
    print(f'For the lower bound group: \nThe correlation coefficent is {l_corr} and the p-value is {l_pvalue}')
    print(f'For the higher bound group: \nThe correlation coefficent is {u_corr} and the p-value is {u_pvalue}')

  def scatter(self, percentile, col_name):
    '''
    Creates a scatter plot of column of interest vs the column that separated the DF by percentile

    Parameters
    ----------
    percentile - int of percentile to separate df by

    col_name - str of column name of interest

    Returns
    -------
    Scatter plot

    '''
    u, l = self.separate_df(percentile)
    fig, ax = plt.subplots()
    ax.scatter(u[self.col_to_separate], u[col_name], alpha=0.5, label='upper bound')
    ax.scatter(l[self.col_to_separate], l[col_name], alpha=0.5, label='lower bound')
    ax.set_title(f'{self.col_to_separate} vs {col_name}')
    ax.set_xlabel(f'{self.col_to_separate}')
    ax.set_ylabel(f'{col_name}')
    ax.legend()
