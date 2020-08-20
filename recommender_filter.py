class Form_filter():
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(data).T
        
    def recommend_by_condition(self, disease_input):
        good_items = []
        for item in self.df.index:
            good = False
            for disease in disease_input:
                if disease in self.df.loc[item]['tag_list']:
                    good = True
            if good == True:
                good_items.append(item)
        return good_items
    
    def filter_allergy(self, allergy_input):
        cannot_eat_items = []
        for item in self.df.index:
            possible = True
            for allergy in user_allergy:
                if allergy in self.df.loc[item]['ingredient']:
                    possible = False
            if possible == False:
                cannot_eat_items.append(item)
        return cannot_eat_items
    
    def final_recommend(self, disease_input, allergy_input):
        good_items = self.recommend_by_condition(disease_input)
        cannot_eat_items = self.filter_allergy(allergy_input)
        final_recommend = {}
        for good in good_items:
            recommend = [item for item in petreat_data[good]['recommend_20'] if item not in cannot_eat_items]
            final_recommend[good] = recommend
        return final_recommend