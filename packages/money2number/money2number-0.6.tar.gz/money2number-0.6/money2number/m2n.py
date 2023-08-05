import re
from word2number import w2n


# class MoneyToNumberzTest:
#     def test_script(self, money_tags):
#         clean_money = MoneyToNumberz.clean_money_tags(money_tags)
#         if clean_money is not None:
#             print('After Cleaning: {}'.format(str(clean_money)))
#         else:
#             print("Couldn't perform the above operation")


class m2n:

    def __init__(self):
        pass

    @staticmethod
    def clean_money_tags(money_tag):
        # removing everything before any number or '$'
        # cleaned_money_tags = []
        try:
            value = re.findall(r'\/$.*|\d.*', money_tag)[0]
            # cleaned_money_tags.append(value)
        except Exception as e:
            value = None
            raise ValueError("Money tags not working?")

        return value

    @staticmethod
    def word2num(each_tag):
        flag = False
        try:
            num = float(w2n.word_to_num(each_tag))
            flag = True
            return num, flag
        except:
            return -1, flag

    @staticmethod
    def get_num(each_tag):
        flag = False
        get_number = re.findall(r'[0-9\.]+', each_tag)
        if not get_number:  # means empty list, couldn't find any number in string
            return get_number, flag
        else:  # means contains only number no word2num conversion needed
            flag = True
            return float(get_number[0]), flag

    @staticmethod
    def process_money_tags(money_tags):
        """
        :param: string containing money term, should be one money term not more than one in a sentence
        :return: list containing real number
        """
        '''
        apply checks....if million like terms available...check number ... if not then go for word
        '''
        # for money_tags in money_tags:
        value = None
        word_num = -1
        try:
            # need to check if number is occuring before million or any word related to money term
            # will be implemented in future updates...  I know this is impt... shutttt upppp!! contribute. :)
            get_number, only_num_flag = m2n.get_num(money_tags)
            word_num, money_word = m2n.word2num(money_tags)

            if money_word & only_num_flag:  # 2.5 million
                value = float(get_number) * word_num
                # return float(get_number) * word_num

            elif money_word:  # thirteen million dollars
                value = word_num

            elif only_num_flag:
                value = get_number

            else:  # if nothing is there in string
                value = None

        except Exception as e:
            raise ValueError("What? Everything failed! What did you input? \n This is the error: {} \n Deal with it.".format(e))

        '''
        Will also be adding wor2number conversion to convert millions billions like that to a complete money related form.
        Let's check if the regex is fine with all or not and find the end cases to cover around all
        '''
        return value


if __name__ == '__main__':
    print(m2n.process_money_tags('here are 12 million dollars'))