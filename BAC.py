############################
# Nich Twatwunnaphong      
# BAC Computation		   
############################

from decimal import Decimal

def file_input():
	"""input file to parsed list
	"""
	file_name = input('Please enter your filename: ')
	in_file = open('files/'+ file_name, encoding='utf-8')
	in_string = in_file.read()

	a_list = in_string.split('\n')

	main_list = []

	for i in a_list:
		b_list = i.split()
		main_list.append(b_list)

	return main_list

def compute_bac(n, w, r):
	"""BAC formula
	"""
	bac = (0.8 * 15 * n * 100) / (w * 1000 * r)

	return bac

def bac_reduction(w, r):
	"""computes BAC reduction per second
	"""
	r_bac = (0.8 * 15 * 1 * 100) / (w * 1000 * r)
	r_bac = (r_bac / 3600.0) 

	return r_bac

def find_time_left(bac, w, r):
	"""finds time left for BAC reset
	"""
	seconds = bac / bac_reduction(w, r)
	seconds = round(seconds, 0)

	m, s = divmod(int(seconds), 60) # a // b, a % b
	h, m = divmod(m, 60)

	#padding
	if(h < 10):
		h = '0' + str(h)

	if(m < 10):
		m = '0' + str(m)

	if(s < 10):
		s = '0' + str(s)

	time_left = str(h) + ':' + str(m) + ':' + str(s)

	return time_left

def find_distribution_ratio(gender):
	"""returns distribution ratio
	"""
	if gender == 'm':
		r= 0.68 
	elif gender == 'f':
		r = 0.55
	else:
		r = 0
	return r

def find_previous_time(time_list, n):
	"""returns index of the closest previous time 
	"""
	diff_list = []
	for i in range(len(time_list)):
		if(time_list[i] > n):
			continue
		diff_list.append(abs(n - time_list[i]))

	return diff_list.index(min(diff_list))

def pad_zeroes(bac):
	"""pads zeroes to BAC 
	"""
	if bac == '0':
		bac = '0.00000'
	bac = bac.ljust(7, '0')

	return bac

def main():
	"""bac-computation
	"""
	p_list = file_input() #list of all inputted values
	case_num = 1
	end_of_file = False

	while not end_of_file:	
		w = float(p_list[0][0])
		gender = p_list[0][1]
		r = find_distribution_ratio(gender)

		total = 0.0

		bac_list = [] #list of all BACs computed
		if float(p_list[1][1]) < 0: # first BAC 
			bac_list.append(0)
		else:
			bac_list.append(compute_bac(float(p_list[1][1]), w, r)) 

		time_list = [] #list of inputted timestamps
		time_list.append(int(p_list[1][0])) #first timestamp

		#header
		print('\nCase ' + str(case_num) + ':',str(w) + 'kg,', gender)
		print('{0:12}'.format('Time'), '{0:12}'.format('Entered'), '{0:8}'.format('Total'), '{0:12}'.format('BAC'), 'Time left')
		
		#main output
		for i in range(1, len(p_list)):
			if p_list[i] != []:
				time = int(p_list[i][0])

			if len(p_list[i]) > 1:
				entered = float(p_list[i][1])
				if not (total + entered < 0):
					total = total + entered
				if i == 1:
					bac = bac_list[0]
				else:
					bac = bac_list[i-2] - ((time - time_list[find_previous_time(time_list, time)]) * bac_reduction(w, r))
					bac = max(0, bac)
					if total + entered < 0:
						bac = bac + compute_bac(0, w, r)
					else:
						bac = bac + compute_bac(entered, w, r)
					bac_list.append(bac)
					time_list.append(time)
				time_left = find_time_left(bac, w, r)
				bac = round(bac, 5)
				bac = pad_zeroes(str(bac))
				print('{0:12}'.format(str(time)), '{0:12}'.format(str(entered)), '{0:8}'.format(str(total)), '{0:12}'.format(bac), time_left)	
				if i == (len(p_list) - 1):
					end_of_file = True

			elif len(p_list[i]) == 0:
				if i == (len(p_list) - 1):
					end_of_file = True
				temp_list = []
				temp_list.extend(p_list[i+1:])
				p_list = temp_list 
				case_num = case_num + 1
				break

			else:
				bac = bac_list[find_previous_time(time_list, time)] - ((time - time_list[find_previous_time(time_list, time)]) * bac_reduction(w, r))
				bac = max(0, bac)
				bac_list.append(bac)
				time_left = find_time_left(bac, w, r)
				bac = round(bac, 5)
				bac = pad_zeroes(str(bac))
				print('{0:12}'.format(str(time)), '{0:12}'.format('-'), '{0:8}'.format('-'), '{0:12}'.format(bac), time_left)
				if i == (len(p_list) - 1):
					end_of_file = True

if __name__ == '__main__':
	main()
