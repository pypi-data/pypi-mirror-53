def print_progress_training(number_iteration=0, index_iteration=0, metrics_acc=0, metrics_loss=0, type_progress=""):
    split_iteration = int((number_iteration*5)/100)
    if split_iteration == 0:
        split_iteration = 1
    progress_bar = "--------------------"
    for i in range(0,index_iteration):
        if i % split_iteration == 0:
            progress_bar = ">" + progress_bar[:-1]
        else:
            progress_bar = progress_bar

    print(str(index_iteration+1)+"/"+str(number_iteration)+"    ["+str(progress_bar)+"]  "+str(type_progress)+"_acc: "+str(metrics_acc)+"       "+str(type_progress)+"_loss: "+str(metrics_loss))
