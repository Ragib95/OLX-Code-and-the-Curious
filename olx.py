import csv
import collections

with open('.\olx-ads-recommendation-dataset\\temp\user_messages.csv', 'rb') as csvfile:
	user_messages = csv.reader(csvfile)
	user_message = collections.defaultdict(list)
	for each in user_messages:
		user_message[each[0]].append(each[1].replace('[', '').replace(']', '').split(', '))
	
	for i in user_message:
		local = []
		for j in user_message[i]:
			local = local + j
		local = collections.Counter(local).most_common(10)
		user_message[i] = [common[0] for common in local]


with open('.\olx-ads-recommendation-dataset\\ads_data.csv', 'rb') as csvfile:
	ads_data= csv.reader(csvfile)
	ads_datas = {}
	ads_status = {}
	for ads in ads_data:
		ads_datas[ads[0]] = ads[1]
		ads_status[ads[0]] = ads[10]



with open('.\olx-ads-recommendation-dataset\user_data.csv', 'rb') as csvfile:
	user_data = csv.reader(csvfile)
	users = collections.defaultdict(list)
	ads_event = {}
	for user in user_data:
		if user[0] != 'event_time':
			value = [user[0], user[7], ads_datas[user[7]]]
			users[user[1]].append(value)
			ads_event[user[1]+user[7]] = user[2]


user_dict = {}
for i in users:
	category = collections.defaultdict(list)
	ads_list = []
	for z in users[i]:
		ads_list.append(z[1])
	ctr = collections.Counter(ads_list)
	for j in users[i]:
		category[j[2]].append([j[0].split(' ')[0], ctr[j[1]], j[1]])
	for k in category:
		category[k].sort(reverse=True)
	user_dict[i] = category

with open('.\olx-ads-recommendation-dataset\\temp\user_messages_test.csv', 'rb') as csvfile:
	user_messages_test = csv.reader(csvfile)

	writer = csv.writer(open("ads_recommendation.csv", 'wb'))
	writer.writerow(['user_id', 'category_id' ,'ads'])
	for each in user_messages_test:
		final_result = []
		if each[0] != 'user_id':
			local = user_dict.get(each[0], "Empty")
			if local != 'Empty':
				local1 = local.get(each[1], 'Empty')
				if local1 != 'Empty':
					for frequent in local1:
						if len(final_result) < 10:
							if frequent[2] not in final_result:
								if ads_status[frequent[2]] == '1':
									if ads_event[each[0]+frequent[2]] == 'view':
										final_result.append(frequent[2])
						else:
							break
				elif local1 == 'Empty':
					final_result = user_message[each[1]]
				
			elif local == 'Empty' or final_result == []:
				final_result = user_message[each[1]]

			if len(final_result) == 0:
				final_result = user_message[each[1]]

			if len(final_result) !=10 :
				for i in user_message[each[1]]:
					if i not in final_result and len(final_result) !=10:
						final_result.append(i)

			writer.writerow([each[0], each[1], str(final_result).replace("'", "")])

print 'Completed, Thanks!'
