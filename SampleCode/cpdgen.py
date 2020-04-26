import random
import plotly.graph_objects as go

if __name__ == "__main__":
    call_list_after_weight = [1200, 2400, 2400, 2400, 3600, 150, 10, 1]
    x_axis = [i for i in range(8)]
    total = 0
    for index in range(8):
        total += call_list_after_weight[index]
    for index in range(8):
        call_list_after_weight[index] = (call_list_after_weight[index]/total)
        if index != 0:
            call_list_after_weight[index] = call_list_after_weight[index] + call_list_after_weight[index-1]
    call_to_make = random.random() #generate a random floating pt. number between 0 and 1
    print(call_list_after_weight)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_axis, y=call_list_after_weight, name='CPD'))
    fig.show()