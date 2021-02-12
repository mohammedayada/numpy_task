from django.shortcuts import render
import numpy as np
# Create your views here.

def home(request):
    if request.method == "POST":
        cd = request.POST
        sequence_1 = cd['seq1']
        sequence_2 = cd['seq2']
        if request.FILES:
            cd = request.FILES
            sequence_1 = str(cd['file1'].read())
            sequence_1 = sequence_1[2:len(sequence_1)-1]
            sequence_2 = str(cd['file2'].read())
            sequence_2 = sequence_2[2:len(sequence_2) - 1]

        main_matrix = np.zeros((len(sequence_1) + 1, len(sequence_2) + 1))
        match_checker_matrix = np.zeros((len(sequence_1), len(sequence_2)))

        match_reward = 1
        mismatch_penalty = -1
        gap_penalty = -2

        for i in range(len(sequence_1)):
            for j in range(len(sequence_2)):
                if sequence_1[i] == sequence_2[j]:
                    match_checker_matrix[i][j] = match_reward
                else:
                    match_checker_matrix[i][j] = mismatch_penalty

        # STEP 1 : Initialisation
        for i in range(len(sequence_1) + 1):
            main_matrix[i][0] = i * gap_penalty
        for j in range(len(sequence_2) + 1):
            main_matrix[0][j] = j * gap_penalty

        # STEP 2 : Matrix Filling
        for i in range(1, len(sequence_1) + 1):
            for j in range(1, len(sequence_2) + 1):
                main_matrix[i][j] = max(main_matrix[i - 1][j - 1] + match_checker_matrix[i - 1][j - 1],
                                        main_matrix[i - 1][j] + gap_penalty,
                                        main_matrix[i][j - 1] + gap_penalty)

        # STEP 3 : Traceback

        aligned_1 = ""
        aligned_2 = ""

        ti = len(sequence_1)
        tj = len(sequence_2)

        while (ti > 0 and tj > 0):

            if (ti > 0 and tj > 0 and main_matrix[ti][tj] == main_matrix[ti - 1][tj - 1] + match_checker_matrix[ti - 1][
                tj - 1]):

                aligned_1 = sequence_1[ti - 1] + aligned_1
                aligned_2 = sequence_2[tj - 1] + aligned_2

                ti = ti - 1
                tj = tj - 1

            elif (ti > 0 and main_matrix[ti][tj] == main_matrix[ti - 1][tj] + gap_penalty):
                aligned_1 = sequence_1[ti - 1] + aligned_1
                aligned_2 = "-" + aligned_2

                ti = ti - 1
            else:
                aligned_1 = "-" + aligned_1
                aligned_2 = sequence_2[tj - 1] + aligned_2

                tj = tj - 1
        context = {
            'res1': aligned_1,
            'res2': aligned_2,
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html')