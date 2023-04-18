import pandas as pd
import numpy as np
def manipulate_features(features):
    data_dict = {'CUST_ID': [features[0]],
                 'BALANCE': [features[1]],
                 'BALANCE_FREQUENCY': [features[2]],
                 'PURCHASES': [features[3]],
                 'ONEOFF_PURCHASES': [features[4]],
                 'INSTALLMENTS_PURCHASES': [features[5]],
                 'CASH_ADVANCE': [features[6]],
                 'PURCHASES_FREQUENCY': [features[7]],
                 'ONEOFF_PURCHASES_FREQUENCY': [features[8]],
                 'PURCHASES_INSTALLMENTS_FREQUENCY': [features[9]],
                 'CASH_ADVANCE_FREQUENCY': [features[10]],
                 'CASH_ADVANCE_TRX': [features[11]],
                 'PURCHASES_TRX': [features[12]],
                 'CREDIT_LIMIT': [features[13]],
                 'PAYMENTS': [features[14]],
                 'MINIMUM_PAYMENTS': [features[15]],
                 'PRC_FULL_PAYMENT': [features[16]],
                 'TENURE': [features[17]]
                 }

    df = pd.DataFrame.from_dict(data_dict)

    df["Monthly_Avg_Purchase"] = df["PURCHASES"]/df["TENURE"]

    df["Monthly_Cash_Advance"] = df["CASH_ADVANCE"]/df["TENURE"]

    def purchasetype(df):
        data_dict = {
            'Purchase_Type_BOTH_ONEOFF_INSTALLMENTS': 0,
            'Purchase_Type_INSTALLMENTS': 0,
            'Purchase_Type_NONE': 0,
            'Purchase_Type_ONEOFF': 0
        }

        for i, row in df.iterrows():
            if (row["ONEOFF_PURCHASES"] == 0) & (row["INSTALLMENTS_PURCHASES"] == 0):
                data_dict['Purchase_Type_NONE'] += 1
            elif (row["ONEOFF_PURCHASES"] > 0) & (row["INSTALLMENTS_PURCHASES"] == 0):
                data_dict['Purchase_Type_ONEOFF'] += 1
            elif (row["ONEOFF_PURCHASES"] == 0) & (row["INSTALLMENTS_PURCHASES"] > 0):
                data_dict['Purchase_Type_INSTALLMENTS'] += 1
            elif (row["ONEOFF_PURCHASES"] > 0) & (row["INSTALLMENTS_PURCHASES"] > 0):
                data_dict['Purchase_Type_BOTH_ONEOFF_INSTALLMENTS'] += 1

        return data_dict

    dummies_data = purchasetype(df)

    dummies = pd.DataFrame(pd.Series(dummies_data)).T


    df["Balance_Credit_Ratio"] = df["BALANCE"]/df["CREDIT_LIMIT"]


    df["Total_Payment_Ratio"] = np.where(df["MINIMUM_PAYMENTS"] == 0,df["MINIMUM_PAYMENTS"], df["PAYMENTS"]/df["MINIMUM_PAYMENTS"])


    #getting the numeric variable names and data
    df_numeric = df._get_numeric_data()

    credit_log = df_numeric.apply(lambda x: np.log(x + 1))

    #merging the log data and dummies data
    creditcarddata_merged = pd.concat([credit_log,dummies],axis = 1)

    ##dropping the variables used to create the KPI
    #var_names = ["BALANCE","PURCHASES","PAYMENTS","MINIMUM_PAYMENTS","PRC_FULL_PAYMENT","TENURE","CASH
    
    var_names = ["BALANCE", "PURCHASES", "PAYMENTS", "MINIMUM_PAYMENTS", "PRC_FULL_PAYMENT", "TENURE", "CASH_ADVANCE", "CREDIT_LIMIT"]
    creditcarddata_new = creditcarddata_merged[[x for x in creditcarddata_merged.columns if x not in var_names]]

    # return the manipulated features
    return creditcarddata_new
    #return creditcarddata_new.values[0].tolist()