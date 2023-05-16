import pandas as pd
import numpy as np
def convert_revenue_range_to_average(revenue_range):
    if pd.isnull(revenue_range):
        return revenue_range
    revenue_range = str(revenue_range)

    if '>' in revenue_range or '<' in revenue_range:
        revenue_range = revenue_range.replace('>', '')
        revenue_range = revenue_range.replace('<', '')
        revenue_range = revenue_range.replace(' ', '')
        revenue_range = revenue_range.replace('$', '')
        revenue_range = revenue_range.replace(',', '')
        if 'B' in revenue_range:
            revenue_range = revenue_range.replace('B', '')
            revenue_range = float(revenue_range) * 1e9
        elif 'M' in revenue_range:
            revenue_range = revenue_range.replace('M', '')
            revenue_range = float(revenue_range) * 1e6
        else:
            revenue_range = float(revenue_range)
        return revenue_range
    elif '-' in revenue_range:
        lower, upper = revenue_range.split(' - ')
        lower = lower.replace(' ', '')
        lower = lower.replace('$', '')
        lower = lower.replace(',', '')
        upper = upper.replace(' ', '')
        upper = upper.replace('$', '')
        upper = upper.replace(',', '')
        if 'B' in lower:
            lower = lower.replace('B', '')
            lower = float(lower) * 1e9
        elif 'M' in lower:
            lower = lower.replace('M', '')
            lower = float(lower) * 1e6
        else:
            lower = float(lower)
        if 'B' in upper:
            upper = upper.replace('B', '')
            upper = float(upper) * 1e9
        elif 'M' in upper:
            upper = upper.replace('M', '')
            upper = float(upper) * 1e6
        else:
            upper = float(upper)
        
        return (lower + upper) / 2
    else:
        revenue_range = revenue_range.replace(' ', '')
        revenue_range = revenue_range.replace('$', '')
        revenue_range = revenue_range.replace(',', '')
        if 'Million' in revenue_range:
            revenue_range = revenue_range.replace('Million', '')
            revenue_range = float(revenue_range) * 1e6
        elif 'Billion' in revenue_range:
            revenue_range = revenue_range.replace('Billion', '')
            revenue_range = float(revenue_range) * 1e9
        elif 'B' in revenue_range:
            revenue_range = revenue_range.replace('B', '')
            revenue_range = float(revenue_range) * 1e9
        elif 'M' in revenue_range:
            revenue_range = revenue_range.replace('M', '')
            revenue_range = float(revenue_range) * 1e6
        
        else:
            revenue_range = float(revenue_range)
        return revenue_range
    
def convert_range_employee_to_average(employees_range):
  if pd.isnull(employees_range):
    return employees_range
  employees_range = str(employees_range)
  employees_range = employees_range.replace(',', '')
  employees_range = employees_range.replace('~', '')
  if '>' in employees_range or '<' in employees_range:
    employees_range = employees_range.replace('>', '')
    employees_range = employees_range.replace('<', '')
    employees_range = employees_range.replace(' ', '')
    employees_range = employees_range.replace(',', '')
    if 'K' in employees_range:
      employees_range = employees_range.replace('K', '')
      employees_range = int(employees_range) * 1e3
    elif 'M' in employees_range:
      employees_range = employees_range.replace('M', '')
      employees_range = int(employees_range) * 1e6
    else:
      employees_range = int(employees_range)
    return employees_range
  elif '-' in employees_range:
    employees_range = employees_range.replace(' ', '')
    employees_range = employees_range.replace(',', '')
    employees_range = employees_range.split('-')
    lower = float(employees_range[0])
    upper = float(employees_range[1])
  elif 'Employees' in employees_range:
    employees_range = employees_range.replace('Employees', '')
    employees_range = employees_range.replace(' ', '')
    
    return int(employees_range)
  else:
    lower = float(employees_range)
    upper = float(employees_range)

  return (lower + upper) / 2

def clean_unique_values(unique_values):
    cleaned_values = []
    formalized_values = []
    # split on - and get the lower and upper bound
    for value in unique_values:
        value = str(value)
        if 'nan' in value:
            continue
        if '$' in value:
            value = value.replace('$', '')
        if '-' in value: 
            lower_bound, upper_bound = value.split('-')
            if ',' in lower_bound:
                lower_bound = lower_bound.replace(',', '')
            if ',' in upper_bound:
                upper_bound = upper_bound.replace(',', '')
            if 'B' in lower_bound:
                lower_bound = lower_bound.replace('B', '')
                lower_bound = float(lower_bound) * 1e9
            elif 'M' in lower_bound:
                lower_bound = lower_bound.replace('M', '')
                lower_bound = float(lower_bound) * 1e6
            if 'B' in upper_bound:
                upper_bound = upper_bound.replace('B', '')
                upper_bound = float(upper_bound) * 1e9
            elif 'M' in upper_bound:
                upper_bound = upper_bound.replace('M', '')
                upper_bound = float(upper_bound) * 1e6
            cleaned_values.append((float(lower_bound), float(upper_bound)))
            formalized_values.append(value)
        if '>' in value:
            if 'B' in value:
                lower_bound = value.replace('B', '')
                if ',' in lower_bound:
                    lower_bound = lower_bound.replace(',', '')
                lower_bound = float(lower_bound.replace('>', '')) * 1e9
                upper_bound = np.inf
            elif 'M' in value:
                lower_bound = value.replace('M', '')
                if ',' in lower_bound:
                    lower_bound = lower_bound.replace(',', '')
                lower_bound = float(lower_bound.replace('>', '')) * 1e6
                upper_bound = np.inf
            else:
                lower_bound = value.replace('>', '')
                if ',' in lower_bound:
                    lower_bound = lower_bound.replace(',', '')
                lower_bound = float(lower_bound)
                upper_bound = np.inf
            cleaned_values.append((float(lower_bound), float(upper_bound)))
            formalized_values.append(value)
        if '<' in value:
            if 'B' in value:
                upper_bound = value.replace('B', '')
                if ',' in upper_bound:
                    upper_bound = upper_bound.replace(',', '')
                lower_bound = 0
                upper_bound = float(upper_bound.replace('<', '')) * 1e9
            elif 'M' in value:
                upper_bound = value.replace('M', '')
                if ',' in upper_bound:
                    upper_bound = upper_bound.replace(',', '')
                lower_bound = 0
                upper_bound = float(upper_bound.replace('<', '')) * 1e6
            else:
                upper_bound = value.replace('<', '')
                if ',' in upper_bound:
                    upper_bound = upper_bound.replace(',', '')
                lower_bound = 0
                upper_bound = float(upper_bound)
            cleaned_values.append((float(lower_bound), float(upper_bound)))
    return cleaned_values, formalized_values
def clean_revenue_range(revenue_range, unique_values, formalized_values):
    # if the value is nan, return nan
    if pd.isnull(revenue_range):
        return revenue_range
    # if the value is not nan get values not range
    revenue_range = str(revenue_range)
    if '-' not in revenue_range and '>' not in revenue_range and '<' not in revenue_range:
        if '$' in revenue_range:
            revenue_range = revenue_range.replace('$', '')
        if ',' in revenue_range:
            revenue_range = revenue_range.replace(',', '')
        if '~' in revenue_range:
            revenue_range = revenue_range.replace('~', '')
        if 'Employees' in revenue_range:
            revenue_range = revenue_range.replace('Employees', '')
        if 'Million' in revenue_range:
            revenue_range = revenue_range.replace('Million', '')
            revenue_range = float(revenue_range) * 1e6
        elif 'M' in revenue_range:
            revenue_range = revenue_range.replace('M', '')
            revenue_range = float(revenue_range) * 1e6
        elif 'Billion' in revenue_range:
            revenue_range = revenue_range.replace('Billion', '')
            revenue_range = float(revenue_range) * 1e9
        elif 'B' in revenue_range:
            revenue_range = revenue_range.replace('B', '')
            revenue_range = float(revenue_range) * 1e9
        else:
            revenue_range = float(revenue_range)
        for i in range(len(unique_values)):
            if revenue_range < unique_values[i][1] and revenue_range > unique_values[i][0]:
                return formalized_values[i] 
        return np.nan
    else:
        if '$' in revenue_range:
            revenue_range = revenue_range.replace('$', '')
        return revenue_range
