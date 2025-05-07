from flask import Flask, render_template, request
import webbrowser
import threading
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from matplotlib.ticker import FormatStrFormatter

# makes the page with flask
app = Flask(__name__)
# makes the main page of the website 
@app.route("/")
def index():
    return render_template("index.html")

# gets data from the html page
@app.route("/submit", methods=['POST'])
def submit():

    """ In this section all the data the user gives will be stored """
    # gets the data for period seperation
    start_of_the_year = 1
    end_of_preperation = int(request.form["End of preperation period"])
    end_of_competition = int(request.form["End of competition period"])
    end_of_rest = 53


    # gets and prosseses the data for the volume of training
    training_volume = request.form['Training Volume']
    # the .split method removes the ',' from the strings and makes them a list
    training_volume = training_volume.split(",")
    # converts the array of strings to integers
    training_volume = [int(value) for value in training_volume]
    
    # gets the data for the weeks that volume will be changed
    volume_weeks = request.form['Volume Weeks']
    volume_weeks = volume_weeks.split(",")
    volume_weeks = [int(value) for value in volume_weeks]


    # gets and prosseses the data for the volume of intensity in training
    training_intensity = request.form['Training Intensity']
    training_intensity = training_intensity.split(",")
    training_intensity = [int(value) for value in training_intensity]
    
    # gets the data for the weeks that intensity will be changed
    intensity_weeks = request.form['Intensity Weeks']
    intensity_weeks = intensity_weeks.split(",")
    intensity_weeks = [int(value) for value in intensity_weeks]
    

    # stores the weeks that the athlete will have test
    testing_weeks_as_a_string = request.form["Weeks for tests"]
    weeks_for_tests = testing_weeks_as_a_string.split(",")
    weeks_for_tests = [int(week) for week in weeks_for_tests]


    # stores the weeks that the athlete will have medical tests to do
    medical_tests_weeks_as_a_string = request.form["Weeks for medical tests"]
    weeks_for_medical_tests = medical_tests_weeks_as_a_string.split(",")
    weeks_for_medical_tests = [int(week) for week in weeks_for_medical_tests]


    # stores the weeks that the athlete will have competitions
    weeks_for_competition_as_a_string = request.form["Weeks for competition"]
    weeks_for_competition = weeks_for_competition_as_a_string.split(",")
    weeks_for_competition = [int(week) for week in weeks_for_competition]
    """ End of data storage collection """
        

    # makes the axes for the figure with width 15 and height 10
    plt.rcParams['figure.figsize'] = [15, 10]
    fig, ax = plt.subplots()

    # seperates the periods with different colors
    plt.bar(0, height= 110,width= end_of_preperation + 1, align='edge', color='#ccffff')
    plt.bar(end_of_preperation + 1, height= 110, width = end_of_competition-end_of_preperation, align='edge', color='#b3ffff')
    plt.bar(end_of_competition + 1, height= 110, width= end_of_rest-end_of_competition, align='edge', color='#99ffff')


    # makes the line graph for training intensity
    plt.plot(intensity_weeks, training_intensity, label='ένταση προπόνησης', color='red')

    # makes the line graph for training volume
    plt.plot(volume_weeks, training_volume, label='όγκος προπόνησης', color='blue')

    # to print the label only one time in the for loop
    weeks_for_tests_label_printed = False
    # makes a bar chart for the weeks that have tests
    for week in weeks_for_tests:
        if not weeks_for_tests_label_printed :
            plt.bar(week, height=1,width=1.0, align='edge',label='εβδομάδες για εξετάσεις επιδόσεων', color='#FF69B4')
            weeks_for_tests_label_printed = True
        else:
            plt.bar(week, height=1,width=1.0, align='edge', color='#FF69B4')

    weeks_for_medical_tests_label_printed = False
    # makes a bar chart for the weeks that have medical tests
    for week in weeks_for_medical_tests:
        if not weeks_for_medical_tests_label_printed:
            plt.bar(week, height=2,width=1.0, align='edge',label='εβδομάδες για ιατρικές εξετάσεις', color='#FFA500')
            weeks_for_medical_tests_label_printed = True
        else:
            plt.bar(week, height=2,width=1.0, align='edge', color='#FFA500')

    weeks_for_competition_tests_label_printed = False
    # makes a bar chart for the weeks that have competitions
    for week in weeks_for_competition:
        if not weeks_for_competition_tests_label_printed:
            plt.bar(week, height=3,width=1.0, align='edge',label='εβδομάδες αγώνων', color='#A020F0')
            weeks_for_competition_tests_label_printed = True
        else:
            plt.bar(week, height=3,width=1.0, align='edge', color='#A020F0')

    # labels the periods for being easily recognized in the  bottom of the graph
    sec = ax.secondary_xaxis(location = 0)
    # to center the name of each period
    sec.set_xticks([(end_of_preperation + start_of_the_year) / 2, ((end_of_competition + 1) + (end_of_preperation + 1)) / 2, (end_of_rest + end_of_competition) / 2], labels=['\n\nΠροετοιμασία', '\n\nΑγώνες', '\n\nΞεκούραση'])
    sec.tick_params('x', length = 0)

    # makes lines for visual seperation of the names of each period
    sec2 = ax.secondary_xaxis(location = 0)
    sec2.set_xticks([0, end_of_preperation + 1, end_of_competition + 1, end_of_rest - 1], labels=[])
    sec2.tick_params('x', length = 40, width = 0.5, color='red')
    ax.set_xlim(-0.6, 8.6)

    # sets the numerical range of x, y axis
    min_persentage = 0
    max_persentage = 105
    start_of_year = 1
    end_of_year = 53

    # sets both axis begining from 0
    ax.set_ylim(ymin = 0)
    ax.set_xlim(xmin = 0)

    # sets the axis step 
    ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax.yaxis.set_ticks(np.arange(min_persentage, max_persentage , 5))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax.xaxis.set_ticks(np.arange(start_of_year, end_of_year , 1))

    plt.legend()
    
    # saves the plot to a string buffer to display it in the html page
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.read()).decode('utf-8')
    plot_url = 'data:image/png;base64,' + plot_url
    # returns the data back to the page to be displayed
    return render_template('index.html', html_data=end_of_preperation, plot_url=plot_url)
    
    

# opens automaticly at localhost:5000 without the need of the user to redirect himself manualy
def open_browser():
    webbrowser.open_new('http://localhost:5000')

# keeps the window open until the program stops
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run()