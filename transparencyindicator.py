# This file converts a range of transparency data to percentages

from data import publishers_ordered_by_title, get_publisher_stats
import timeliness
import forwardlooking
import comprehensiveness


def is_number(s):
    """ @todo Document this function
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def convert_to_int(x):
    """ @todo Document this function
    """
    if is_number(x):
        return int(x)
    else:
        return 0


def table():
    """Generate data for the publisher forward-looking table
    """

    # Store timeliness data in variable
    timeliness_frequency_data = timeliness.publisher_frequency_dict()
    timeliness_timelag_data = timeliness.publisher_timelag_dict()

    # Store generator objects for the data that we are receiving
    forwardlooking_data = forwardlooking.table()
    comprehensiveness_data = comprehensiveness.table()

    # Loop over each publisher
    for publisher_title, publisher in publishers_ordered_by_title:

        # Store the data for this publisher as a new variable
        publisher_stats = get_publisher_stats(publisher)
        
        # Create a list for publisher data, and populate it with basic data
        row = {}
        row['publisher'] = publisher
        row['publisher_title'] = publisher_title

        # Compute timeliness statistic
        # Assign frequency score
        if timeliness_frequency_data[publisher][3] == 'Monthly':
            frequency_score = 4
        elif timeliness_frequency_data[publisher][3] == 'Quarterly':
            frequency_score = 3
        elif timeliness_frequency_data[publisher][3] == 'Six-Monthly':
            frequency_score = 2
        elif timeliness_frequency_data[publisher][3] == 'Annual':
            frequency_score = 1
        else: # timeliness_frequency_data[publisher][3] == 'Less than Annual' or something else!
            frequency_score = 0

        # Assign timelag score
        if timeliness_timelag_data[publisher][3] == 'One month':
            timelag_score = 4
        elif timeliness_timelag_data[publisher][3] == 'A quarter':
            timelag_score = 3
        elif timeliness_timelag_data[publisher][3] == 'Six months':
            timelag_score = 2
        elif timeliness_timelag_data[publisher][3] == 'One year':
            timelag_score = 1
        else: # timeliness_timelag_data[publisher][3] == 'More than one year' or something else!
            timelag_score = 0

        # Compute the percentage
        row['timeliness'] = int( (float(frequency_score + timelag_score) / 8) * 100 )


        # Compute forward looking statistic
        # Get the forward looking data for this publisher 
        publisher_forwardlooking_data = forwardlooking_data.next()

        # Convert the data for this publishers 'Percentage of current activities with budgets' fields into integers
        numbers = [ int(x) for x in publisher_forwardlooking_data['year_columns'][2].itervalues() if is_number(x) ]
        
        # Compute and store the mean average for these fields
        row['forwardlooking'] = sum(int(y) for y in numbers) / len(publisher_forwardlooking_data['year_columns'][2])


        # Compute comprehensive statistic
        # Get the comprehensiveness data for this publisher 
        publisher_comprehensiveness_data = comprehensiveness_data.next()

        # Compute and store the mean average for the average fields. Note 'core_average' has a double weighting
        row['comprehensive'] = ( (convert_to_int(publisher_comprehensiveness_data['core_average']) * 2) + publisher_comprehensiveness_data['financials_average'] + publisher_comprehensiveness_data['valueadded_average'] ) / 4


        # Compute score
        row['score'] = int( (row['timeliness'] + row['forwardlooking'] + row['comprehensive']) / 3 )

        # Store the coverage data
        row['coverage'] = int(publisher_stats['coverage'])

        # Compute Coverage-adjusted score
        row['score_coverage_adjusted'] = int( row['score'] * int(row['coverage'] / 100) ) 


        # Return a generator object
        yield row
