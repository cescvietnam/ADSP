import numpy as np
from one_bit_encoding import one_bit_encoding
import copy



def viterbi_decoding_hard_input(double_frame, function_matrix = np.ones((2,3))):
	paths = [[]]
	total_errors = [0]
	s_lists = [[0]*(function_matrix.shape[1]-1)]
	bits = [0, 1]
	R = function_matrix.shape[0] - 1
	for i in range(0, double_frame.shape[0], function_matrix.shape[0]):
		temp_paths = []
		temp_total_errors = []
		temp_s_lists = []
		chunk = double_frame[i:i + R + 1]
		for j, current_path in enumerate(paths):
			s_list = s_lists[j]
			current_total_error = total_errors[j]
			for bit in bits:
				output, temp_s_list = one_bit_encoding(bit, s_list, function_matrix)
				temp_total_error = current_total_error + int(sum(abs(chunk - output)))
				temp_path = copy.copy(current_path)
				temp_path.append(bit)
				if temp_s_list not in temp_s_lists:
					temp_paths.append(temp_path)
					temp_total_errors.append(temp_total_error)
					temp_s_lists.append(temp_s_list)
				else:
					idx = temp_s_lists.index(temp_s_list)
					if temp_total_errors[idx] > temp_total_error:
						temp_paths[idx] = temp_path
						temp_total_errors[idx] = temp_total_error
		paths = temp_paths
		s_lists = temp_s_lists
		total_errors = temp_total_errors
	min_error = min(total_errors)
	min_error_index = total_errors.index(min_error)
	return np.array(paths[min_error_index])

def viterbi_decoding_soft_input(double_frame, function_matrix = np.ones((2,3))):
	paths = [[]]
	total_scores = [0]
	s_lists = [[0]*(function_matrix.shape[1]-1)]
	bits = [0, 1]
	R = function_matrix.shape[0] - 1
	for i in range(0, double_frame.shape[0], function_matrix.shape[0]):
		temp_paths = []
		temp_total_scores = []
		temp_s_lists = []
		chunk = double_frame[i:i + R + 1]
		for j, current_path in enumerate(paths):
			s_list = s_lists[j]
			current_total_score = total_scores[j]
			for bit in bits:
				output, temp_s_list = one_bit_encoding(bit, s_list, function_matrix)
				temp_total_score = current_total_score
				for k, output_bit in enumerate(output):
					if output_bit==0:
						temp_total_score = temp_total_score - chunk[k]
					else:
						temp_total_score = temp_total_score + chunk[k]
				temp_path = copy.copy(current_path)
				temp_path.append(bit)
				if temp_s_list not in temp_s_lists:
					temp_paths.append(temp_path)
					temp_total_scores.append(temp_total_score)
					temp_s_lists.append(temp_s_list)
				else:
					idx = temp_s_lists.index(temp_s_list)
					if temp_total_scores[idx] < temp_total_score:
						temp_paths[idx] = temp_path
						temp_total_scores[idx] = temp_total_score
		paths = temp_paths
		s_lists = temp_s_lists
		total_scores = temp_total_scores
	max_score = max(total_scores)
	max_error_index = total_scores.index(max_score)
	return np.array(paths[max_error_index])






