# imports
# dcc = dash core components - the interactive elements such as drop downs
import dash
import datetime as dt
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import zipfile as zf

# load data 
zf = zf.ZipFile('cleaned/cleaned.csv.zip') 
df = pd.read_csv(zf.open('cleaned.csv'), index_col=[0])

# setup
app =  dash.Dash(__name__, title='Dash App')
server = app.server

# initialize
app = dash.Dash()

# drop down below for bullet point one = I have hard coded which is ok because the values won't change --> use as justification in read me
# layout
app.layout = html.Div([
    html.H1('Sales Data Analysis'),
    
    html.Button('Click to plot product\category purchases graph', id='plot_graph_btn'),
    html.Div(id='out', children = []),
    dcc.Graph(figure={}, id='graph_set_one'),
    
    html.Button('Click to plot branches sales graph', id='plot_graph_btn2'),
    html.Div(id='out2', children = []),
    dcc.Graph(figure={}, id='graph_set_two'),
    
    html.Button('Click to plot per hour sales graph', id='plot_graph_btn3'),
    html.Div(id='out3', children = []),
    dcc.Graph(figure={}, id='graph_set_three'),
    
    html.Button('Click to plot profitable branches', id='plot_graph_btn4'),
    html.Div(id='out4', children = []),
    dcc.Graph(figure={}, id='graph_set_four'),
    
    dcc.Dropdown( options=[
        {'label': 'South East England', 'value': 'South East England'},
        {'label': 'North East England', 'value': 'North East England'},
        {'label': 'East of England', 'value': 'East of England'},
        {'label': 'Wales', 'value': 'Wales'},
        {'label': 'London', 'value': 'London'},
        {'label': 'West Midlands', 'value': 'West Midlands'},
        {'label': 'Northern Ireland', 'value': 'Northern Ireland'},
        {'label': 'East of England', 'value': 'East of England'},
        # to show all region data if required
        {'label': 'overall', 'value': 'overall'}],
        id='region-drop-down',
        ),
    dcc.Dropdown( options=[
        {'label': 'Most Purchased', 'value': 'Most Purchased'},
        {'label': 'Least Purchased', 'value': 'Least Purchased'}],
        id='most_and_least_purchased_dropdown'
        ),
    dcc.Dropdown( options=[
        {'label': 'product', 'value': 'product'},
        {'label': 'category', 'value': 'category'}],
        id='product_and_product_category_dropdown'
        ),
    dcc.Dropdown( options=[
        {'label': 'Most Sales in amount ', 'value': 'Most amount'},
        {'label': 'Most Sales in quantity', 'value': 'Most quantity'},
        {'label': 'least Sales in quantity', 'value': 'Least quantity'},
        {'label': 'least Sales in amount', 'value': 'Least amount'}],
        id='most_least_sales'
        ),    
    ])

# # callbacks -- BULLET POINT 1 least and most purchased product/product category per region

# have all three (dropdowns) as states and the button as the input
@app.callback (
    # output
    Output(component_id='graph_set_one', component_property='figure'),
    Output(component_id='out', component_property='children'),
    # input
    Input(component_id='plot_graph_btn', component_property='n_clicks'),
    State(component_id='region-drop-down', component_property='value'),
    State(component_id='most_and_least_purchased_dropdown', component_property='value'),
    State(component_id='product_and_product_category_dropdown', component_property='value'),
)
# if button is clicked and region is selected show the data for the region selected otherwise show data for the other option and same for all the others

def purchase(button, region, most_least, prod_prod_cat):
    if button is not None:
        
        
        # Imports cleaned data
        # df = pd.read_csv('cleaned/cleaned.csv', index_col=0)
        # filter the data. Looks at my data_frame and filter's based on the region column. If overall has not been selected
        # otherwise use all data
        if region != 'overall':
            region_data = df[df['region'] == region ]
        else:
            # assigning the data frame using the variable name defined above
            region_data = df
        # pivot table summarises data. index is the thing that you want to make a summary of so in this case it will be by product or product category
        purchases = region_data.pivot_table(index= prod_prod_cat, columns= None, values= 'amount', aggfunc= np.sum)
        # reset index so that the index above goes back in to the mix for the next selection
        purchases = purchases.reset_index()
        # sorts from lowest to highest
        ascending = True
        # if user selects most purchased 
        if most_least == 'Most Purchased':
            # sorts from highest to lowest
            ascending = False
        # ascending = ascending simply means that it will equal to what the person selected
        purchases =  purchases.sort_values(by = 'amount', ascending = ascending).head(10)
        # returns graph and Div text as children 
        return px.bar(purchases, x= prod_prod_cat, y='amount'), "Purchases Graph Was plotted"

# ----------------------------------------------------------------------

# callbacks -- BULLET POINT 2 performing top and bottom 10 quantity and money made from sales
@app.callback (
    # output
    Output(component_id='graph_set_two', component_property='figure'),
    Output(component_id='out2', component_property='children'),
    # input
    Input(component_id='plot_graph_btn2', component_property='n_clicks'),
    State(component_id='region-drop-down', component_property='value'),
    State(component_id='most_least_sales', component_property='value'),
#     State(component_id='branches_dropdown', component_property='options'),
)

def sales(button, region, most_least,):
    if button is not None:
        # df = pd.read_csv('cleaned/cleaned.csv', index_col=0)
        # filter the data. Looks at my data_frame and filter's based on the region column 
        if region != 'overall':
            region_data = df[df['region'] == region ]
        else:
            region_data = df
        # pivot table summarises data. index is the thing that you want to make a summary of so in this case
        sales = region_data.pivot_table(index= 'branch_name', columns= None, values= ['amount','quantity'], aggfunc= np.sum)
        # reset index so that the index above goes back in to the mix for the next selection
        sales = sales.reset_index()
        # if user selects most purchased 
        if most_least == 'Most amount':
#             sorts from highest to lowest
            ascending = False
            y_axis = 'amount'
        elif most_least == 'Least amount':
#             sorts from lowest to highest
            ascending = True
            y_axis = 'amount'
        elif most_least == 'Least quantity':
#             sorts from lowest to highest
            ascending = True
            y_axis = 'quantity'
        elif most_least == 'Most quantity':
#             sorts from lowest to highest
            ascending = False
            y_axis = 'quantity'
               
        # ascending = ascending simply means that it will equal to what the person selected
        sales =  sales.sort_values(by = y_axis, ascending = ascending).head(10)
        return px.bar(sales, x= 'branch_name', y=y_axis), 'Sales Graph was plotted'
# ----------------------------------------------------------------------

# callbacks -- BULLET POINT 3 per hour sales top and bottom 10 branches
# NEEDS TO DISPLAY X=hours and Y=sales -> drop down to determine which branch date is visualised
@app.callback (
    # output
    Output(component_id='graph_set_three', component_property='figure'),
    Output(component_id='out3', component_property='children'),
    # input
    Input(component_id='plot_graph_btn3', component_property='n_clicks'),
)

def hourl_sales(button_click):
    if button_click is not None:
        # df = pd.read_csv('cleaned/cleaned.csv', index_col=0)
        # get top branches by amount
        branches = df.pivot_table(index= 'branch_name', columns= None, values= ['amount'], aggfunc= np.sum)
    hourly_sales = []
    # run loop for all branches
    for i in range(len(branches)):
        # assign variable to branch names and total sales
        # i = count
        branch_name = branches.index[i]
        total_sales = branches.values[i][0]
        # select data from each branch 
        branch_data = df[df['branch_name'] == branch_name]
        # to calculate number of hours in total - gets first and last line and assign them to datetime variable.
        r1 = branch_data.sort_values(['year', 'month','day'])[:1]
        r2 = branch_data.sort_values(['year', 'month','day'])[-1:]
        first_sale_time = dt.datetime(r1['year'].values[0],r1['month'].values[0],r1['day'].values[0],r1['hour'].values[0])
        last_sale_time = dt.datetime(r2['year'].values[0],r2['month'].values[0],r2['day'].values[0],r2['hour'].values[0])
        # calculation to calculate total number of hours between first sale time and last sale time
        diff = last_sale_time - first_sale_time
        total_hours = diff.days * 24 + diff.seconds // 3600
        # appends hourly sales array after calculating per hour sales 
        hourly_sales.append(total_sales/total_hours)

    # use array appended in the loop and creates a new column in the data frame
    branches['hourly_sales'] = hourly_sales
    # reset index and sort values by hourly sales in order of highest to lowest
    branches = branches.reset_index().sort_values('hourly_sales', ascending = False)
    # create graph and return graph along with the Div text as children
    figure = px.bar(branches, x='hourly_sales', y='branch_name')
    return figure, 'hourly_sales ploted'

# ----------------------------------------------------------------------

# # callbacks -- BULLET POINT 4 top and bottom 10 profitable branches

@app.callback (
    # output
    Output(component_id='graph_set_four', component_property='figure'),
    Output(component_id='out4', component_property='children'),
    # input
    Input(component_id='plot_graph_btn4', component_property='n_clicks'),
)

def profitable_branches(button_click):
    if button_click is not None:
        # df = pd.read_csv('cleaned/cleaned.csv', index_col=0)
        branches = df.pivot_table(index= 'branch_name', columns= None, values= ['amount'], aggfunc= np.sum)
        # load branch expenses file because file became to big when trying to merge with cleaned data files
        b_exp = pd.read_csv('cleaned/branch_expenses.csv')
        # add all expenses and create new column with combined totals
        b_exp['total_expenses'] = b_exp.operational_cost+b_exp.staff_bonuses+b_exp.misc_expenses+b_exp.waste_cost
        # group total expenses by branch name
        b_exp = b_exp.pivot_table(index= 'branch_name', columns= None, values= ['total_expenses'], aggfunc= np.sum)
        # merge both pivot tables that were grouped by branch name
        new_df = b_exp.reset_index().merge(branches.reset_index())
        # rename amount column to total sales for reabability purposes
        new_df.rename(columns={"amount":"total_sales"},inplace=True)
        # create a new column 'profits' and calculate sales less expenses
        new_df['profits'] = new_df.total_sales-new_df.total_expenses

        figure = px.bar(new_df.sort_values('profits').head(10), x='profits', y='branch_name')
        return figure, 'top branches profit ploted'

# ----------------------------------------------------------------------


# running
if __name__ == '__main__':
    app.run_server(debug=True)