import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.dummy import DummyRegressor
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.metrics import confusion_matrix
#from sklearn.metrics import roc_curve
from sklearn.model_selection import cross_val_score, train_test_split
import warnings
warnings.filterwarnings('ignore')
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn import neighbors
#from sklearn.model_selection import cross_val_score
from itertools import repeat

# Main function starts here ->
def main(): # TK, LB
    print('Program has started...')
    pre_processing() # pre process the data
    linear_knn_regression() # linear regression and knn regression
    lasso_regression() # lasso regression
    ridge_regression() # ridge regression
    print('Program has finished...')
    return

# Preprocessing function starts here
def pre_processing(): # LB
    # Load data from datasets
    wea = pd.read_csv('weather.csv')
    count_2019 = pd.read_csv('2019_cycle_counter.csv')
    count_2020 = pd.read_csv('2020_cycle_counter.csv')
    count_2021 = pd.read_csv('2021_cycle_counter.csv')

    # load in the weather data and discard all the rows corresponding to dates before january 1st 2019
    relevant_index = 23 + 245448
    daylight_saving_time_index = 2137
    wea_date = wea.iloc[relevant_index:,0] # load 1st column, date
    wea_date = wea_date.drop(wea_date.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_rain = wea.iloc[relevant_index:,2] # load 3rd column, precipitation amount (rain)
    wea_rain = wea_rain.drop(wea_rain.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_temperature = wea.iloc[relevant_index:,4] # load 5th column, temperature
    wea_temperature = wea_temperature.drop(wea_temperature.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_humidity = wea.iloc[relevant_index:,9] # load 10th column, relative humidity
    wea_humidity = wea_humidity.drop(wea_humidity.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_wind_speed = wea.iloc[relevant_index:,12] # load 13th column, mean wind speed
    wea_wind_speed = wea_wind_speed.drop(wea_wind_speed.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_wind_direction = wea.iloc[relevant_index:,14] # load 15th column, wind direction
    wea_wind_direction = wea_wind_direction.drop(wea_wind_direction.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_sun_duration = wea.iloc[relevant_index:,17] # load 18th column, sun duration
    wea_sun_duration = wea_sun_duration.drop(wea_sun_duration.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_visibility = wea.iloc[relevant_index:,18] # load 19th column, visibility
    wea_visibility = wea_visibility.drop(wea_visibility.index[daylight_saving_time_index]) # drop daylight saving time error
    wea_cloud_amount = wea.iloc[relevant_index:,20] # load 21st column, cloud amount
    wea_cloud_amount = wea_cloud_amount.drop(wea_cloud_amount.index[daylight_saving_time_index]) # drop daylight saving time error

    # load in cycle count data for 2019
    count_date_2019 = count_2019.iloc[:,0] # load 1st column, date
    count_grt_2019 = count_2019.iloc[:,1] # load 2nd column, Grove Road Totem (grt) location
    count_nsrs_2019 = count_2019.iloc[:,2] # load 3rd column, North Strand Rd S/B (nsrs) location
    count_nsrn_2019 = count_2019.iloc[:,3] # load 4th column, North Strand Rd N/B (nsrn) location
    count_cm_2019 = count_2019.iloc[:,4] # load 5th column, Charleville Mall (cm) location
    count_gs_2019 = count_2019.iloc[:,5] # load 6th column, Guild Street (gs) location
    total_count_2019 = count_2019.sum(axis=1) # calculate the total amount for each row

    # load in cycle count data for 2020
    count_date_2020 = count_2020.iloc[:,0] # load 1st column, date
    count_cm_2020 = count_2020.iloc[:,1] # load 2nd column, Charleville Mall (cm) location
    count_grt_2020 = count_2020.iloc[:,4] # load 5th column, Grove Road Totem (grt) location
    count_gs_2020 = count_2020.iloc[:,7] # load 8th column, Guild Street (gs) location
    count_nsrn_2020 = count_2020.iloc[:,10] # load 11th column, North Strand Rd N/B (nsrn) location
    count_nsrs_2020 = count_2020.iloc[:,11] # load 12th column, North Strand Rd S/B (nsrs) location
    column_list_2020 = list(count_2020) # get all the columns from the 2020 dataset
    column_list_2020.remove('Charleville Mall Cyclist IN') # remove IN as already counted
    column_list_2020.remove('Charleville Mall Cyclist OUT') # remove OUT as already counted
    column_list_2020.remove('Grove Road Totem OUT') # remove OUT as already counted
    column_list_2020.remove('Grove Road Totem IN') # remove IN as already counted
    column_list_2020.remove('Guild Street bikes IN-Towards Quays') # remove IN as already counted
    column_list_2020.remove('Guild Street bikes OUT-Towards Drumcondra') # remove OUT as already counted
    total_count_2020 = count_2020[column_list_2020].sum(axis=1) # sum up total of totals

    # load in cycle count data for 2021
    count_date_2021 = count_2021.iloc[:,0] # load 1st column, date
    count_cm_2021 = count_2021.iloc[:,1] # load 2nd column, Charleville Mall (cm) location
    count_d1_2021 = count_2021.iloc[:,4] # load 5th column, Drumcondra 1 (d1) location
    count_d2_2021 = count_2021.iloc[:,7] # load 8th column, Drumcondra 2 (d2) location
    count_grt_2021 = count_2021.iloc[:,10] # load 11th column, Grove Road Totem (grt) location
    count_nsrn_2021 = count_2021.iloc[:,13] # load 14th column, North Strand Rd N/B (nsrn) location
    count_nsrs_2021 = count_2021.iloc[:,14] # load 15th column, North Strand Rd S/B (nsrs) location
    count_r1_2021 = count_2021.iloc[:,15] # load 16th column, Richmond Street 1 (r1) location
    count_r2_2021 = count_2021.iloc[:,18] # load 19th column, Richmond Street 2 (r2) location
    column_list_2021 = list(count_2021) # all the columns from the 2021 dataset
    column_list_2021.remove('Charleville Mall Cyclist IN') # remove IN as already counted
    column_list_2021.remove('Charleville Mall Cyclist OUT') # remove OUT as already counted
    column_list_2021.remove('Drumcondra Cyclists 1 Cyclist IN') # remove IN as already counted
    column_list_2021.remove('Drumcondra Cyclists 1 Cyclist OUT') # remove OUT as already counted
    column_list_2021.remove('Drumcondra Cyclists 2 Cyclist IN') # remove IN as already counted
    column_list_2021.remove('Drumcondra Cyclists 2 Cyclist OUT') # remove OUT as already counted
    column_list_2021.remove('Grove Road Totem OUT') # remove OUT as already counted
    column_list_2021.remove('Grove Road Totem IN') # remove IN as already counted
    column_list_2021.remove('Richmond Street Cyclists 1 Cyclist IN') # remove IN as already counted
    column_list_2021.remove('Richmond Street Cyclists 1 Cyclist OUT') # remove OUT as already counted
    column_list_2021.remove('Richmond Street Cyclists 2  Cyclist IN') # remove IN as already counted
    column_list_2021.remove('Richmond Street Cyclists 2  Cyclist OUT') # remove OUT as already counted
    total_count_2021 = count_2021[column_list_2021].sum(axis=1) # sum up total of totals
    
    total_count_2021 = total_count_2021[:-503] # remove the last 503 rows since we only have weather data until 1/10/2021 00:00
    count_date_2021 = count_date_2021[:-503] # remove the last 503 rows since we only have weather data until 1/10/2021 00:00

    count_date_total = count_date_2019.append(count_date_2020.append(count_date_2021)) # combine 2019, 2020 and 2021 dates into one list
    total_count = total_count_2019.append(total_count_2020.append(total_count_2021)) # combine total count from 2019, 2020 and 2021
    
    frame = { 'Date & Time': wea_date, 'Rain': wea_rain, 'Temperature': wea_temperature, 'Humidity': wea_humidity, 
        'Wind Speed': wea_wind_speed, 'Wind Direction': wea_wind_direction, 'Sun Duration': wea_sun_duration, 
        'Visibility': wea_visibility, 'Cloud Amount': wea_cloud_amount, 'Total Count': total_count.tolist() } # combine columns into a frame
    result = pd.DataFrame(frame) # add frame to dataframe
    result['Date & Time'] = result['Date & Time'].str.replace('-','/') # replace the dashes with forward slashes so the two formats are the same
    result['Date & Time'] = result['Date & Time'].str.replace(r'(\d{2}):(\d{2}):(\d{2})', r'\1:\2', regex=True) # delete the :ss since they are all 00 seconds which doesn't provide more information
    result.to_csv('results.csv', index=False) # write dataframe to csv file 
    print('Finished preprocessing data...')

def linear_knn_regression(): # LB
    print('Starting linear and knn regression...')
    # ----------------------------------------------------------------------------#
    ############################ Initialization ###################################
    # ----------------------------------------------------------------------------#
    result = pd.read_csv('results.csv') # read preprocessed data
    y = result.iloc[:,9] # read the count (output)
    X = result.iloc[:,0:9] # read in all the other columns (inputs)
    X['Date & Time'] = X['Date & Time'].str[11:-3] # truncate date and time to only the hours

    k_values = list(range(1, 21)) # create a list from 1 to 20 for different k values
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2) # split data into training and test data
    temp = [] # init array for errors
    lr_mean = [] # mean error linear regression
    lr_std = [] # std error linear regression
    knn_mean = [] # mean error knn
    knn_std = [] # std error knn
    dummy_mean_mean = [] # mean error mean
    dummy_mean_std = [] # std error mean
    dummy_median_mean = [] # mean error median
    dummy_median_std = [] # mean std median
    kf = KFold(n_splits=5) # 5 splits for kfold
    lr_model = LinearRegression() # initialize linear regression model
    dummy_mean = DummyRegressor(strategy='mean') # dummy mean model
    dummy_median = DummyRegressor(strategy='median') # dummy median model

    # ----------------------------------------------------------------------------#
    ############################ Linear Regression ################################
    # ----------------------------------------------------------------------------#
    for train, test in kf.split(x_train): # perform 5-fold cross validation on training data
        lr_model.fit(x_train.iloc[train], y_train.iloc[train]) # fit the training data
        y_pred_lr = lr_model.predict(x_train.iloc[test]) # predict using test data
        temp.append(metrics.mean_squared_error(y_train.iloc[test], y_pred_lr)) # add error to temp array
    lr_mean.extend(repeat(np.mean(temp), len(k_values))) # extend for straight line for linear regression
    lr_std.extend(repeat(np.std(temp), len(k_values))) # extend for straight line for linear regression
    coeff = pd.DataFrame(lr_model.coef_, X.columns, columns=['Coeff']) # save coefficients of each input feature
    

    # ----------------------------------------------------------------------------#
    ############################ KNN Regression ###################################
    # ----------------------------------------------------------------------------#    
   
    for k in k_values: # for each k value
        temp = [] # temp array to store errors
        knn_model = neighbors.KNeighborsRegressor(n_neighbors=k) # init model
        for train, test in kf.split(x_train): # perform 5-fold cross validation on training data
            knn_model.fit(x_train.iloc[train], y_train.iloc[train]) # fit model on training data
            y_pred_knn = knn_model.predict(x_train.iloc[test]) # predict on test data
            temp.append(metrics.mean_squared_error(y_train.iloc[test], y_pred_knn)) # add error to temp array
        knn_mean.append(np.mean(temp)) # add mean of estimates
        knn_std.append(np.std(temp)) # add std of estimates
    

    # ----------------------------------------------------------------------------#
    ############################ Dummy Regressors #################################
    # ----------------------------------------------------------------------------#
    dummy_mean.fit(x_train, y_train) # fit model
    dummy_median.fit(x_train, y_train) # fit model

    y_pred_mean = dummy_mean.predict(x_test) # make prediction
    y_pred_median = dummy_median.predict(x_test) # make prediction

    mean_mean_rmse = np.mean(metrics.mean_squared_error(y_pred_mean, y_test)) # mean rmse dummy mean
    median_mean_rmse = np.mean(metrics.mean_squared_error(y_pred_median, y_test)) # mean rmse dummy median
    
    mean_std_rmse = np.std(metrics.mean_squared_error(y_pred_mean, y_test)) # std rmse dummy mean
    median_std_rmse = np.std(metrics.mean_squared_error(y_pred_median, y_test)) # std rmse dummy median
    
    dummy_mean_mean.extend(repeat(mean_mean_rmse, len(k_values))) # extend for straight line for dummy mean
    dummy_mean_std.extend(repeat(mean_std_rmse, len(k_values))) # extend for straight line for dummy mean
    
    dummy_median_mean.extend(repeat(median_mean_rmse, len(k_values))) # extend for straight line for median
    dummy_median_std.extend(repeat(median_std_rmse, len(k_values))) # extend for straight line for median
    

    # ----------------------------------------------------------------------------#
    ############################ Plot and Compare #################################
    # ----------------------------------------------------------------------------#

    plt.errorbar(k_values, dummy_mean_mean, yerr=dummy_mean_std, label='Dummy mean') # plot error bar for mean
    plt.errorbar(k_values, dummy_median_mean, yerr=dummy_median_std, label='Dummy median') # plot error bar for median
    plt.errorbar(k_values, lr_mean, yerr=lr_std, label='Linear Regression') # plot error bar for linear regression
    plt.errorbar(k_values, knn_mean, yerr=knn_std, label='KNN classifier') # plot errorbar for knn
    plt.legend() # plot legend
    plt.xlabel('k values') # set x label
    plt.ylabel('Mean square error') # set y label
    plt.title('Comparison of Root Mean Squared Error (RMSE) \nfor different models vs different k values') # set title
    plt.show() # show plot

    print('Finished linear and knn regression')

def lasso_regression(): # CT, TK
    print('Starting lasso regression...')
    # Use cross validation to select hyperparameters
    # Compare performance against baseline predictors
    print('Finished lasso regression...')

def ridge_regression(): # TK, CT
    print('Starting ridge regression...')
    # Use cross validation to select hyperparameters
    # Compare performance against baseline predictors
    print('Finished ridge regression...')

if __name__ == '__main__':
    main()
