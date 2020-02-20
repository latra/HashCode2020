#import xrange
import math
from dataset import Dataset

class Library:
    def __init__(self, library_id, books, books_in_parallel, time):
        self.id = library_id
        self.books = books.sort()
        self.books_in_parallel = books_in_parallel
        self.time = time

    def get_punctuation(availible_time, scanned_books):
        punctuation = 0
        for i in math.ceil(int(len(self.books)/self.books_in_parallel)):
            position = i*self.books_in_parallel
            if position+self.books_in_parallel < len(books):
                puntuation = puctuation + self.sum_punctuations(self.books[position])

def main():
    datasetURLs = [
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv96z2wILTmc0q35abZk6s8nklnGSRLd0IKa2jein6k8THmQLBlLCj144Yi8ih04jwPxn0ubGUsOWVha5w7UOMt0oLsSYtafv_oqVogstm7ve0br1JiNJ8IRE55Fgq2i6zRGNCTwjOU0gJJuRvevzTcP2Cq8_l5f9UcHJbfOfB0sq4evSBNx8gBMXZzNLUfpKppv848Z4XQ2Eh6e6qwfZO2QXbGnjnxuWNBDXYzdiMYd6CHI6qIHmY9K8pr81n4IaR9nF0_uESJ87ckK0lkNSX1c5VpCCfDxmVCM6DyYr2uWzEv15FKB0z0grxBdIy7Ek0M_L5GdR",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94kPv9bNHpmvuYRrlBfNhpxJTP3rqdEnAvWKPOmvlXWKTh4B3r-zEpdPVLqCmRr2a2U6NlmOseGUaKgA2MBL1R0smk2Yp5T4BBM5ksZ1ORlFESooGzvy7FMkB8QdideiU7DRpYIMBZ9n6iPDrJFYwWcvCa0lHkvFJkNVDhewrTmeunr24d_LaIVyKZ0DUiD9LSRFQXdG7aHc_7mnNPsv9j0l4LZCpFgdPDuA_i3Iowsi-dw7Jz9jiXhUO24DPm7iHoTqTB6hYGnkR-sUl1AJjFWa7q4xbe2EI3gh-ctcvdrIP92gE60ALO_-K57K6-esBJiYVqx",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv95NC_WFM6Jsbq9RYjiBXGn1NaSHn6ZUu2NGyX_ez-9YgExaDbROx5QHPAb5UbBCOj4JXU25gZZN0a-q7x_CqqtG9DfLsewBlNb-bGTpBidu1rGh8UWRVB8P4z39RUaZYu3C7UuhE9WF4aUUmA1Xq847HKJDqJ22ksunXBGAnYI61yglZp_wOyzmdp0i_tRSmlO-Jj60bzgB084z3GUYfy00_Kih1c0f7g3iHIPr4FjlxY_4s4rZcJp29yrJHp_dDGZPGsK65tmtmK5c1kptuin39knpKc0tQ2hmJhV-YBNtvyVCvc-wVoM-0f4GsSCbUMnGmu-r",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94EswDoarsD_T8xfMl8Lx_Bb1V9ppyCMQuCsTXwowKBQ_JFwr9PzEVxgeAgwIeUbZU6R6sg2vrGKpBVKjpwfRfqJxFHOEobK82DVjKwLgi5jkGw3W3td09e18wF_xRXHtC2vewVhS0CyLoju7ykI9qLhZlaJI5ITzOSEKsPlT5sgkjCPFMK10ebbniYT4wKFAFGEMLkIolRCkgVAO0Fo2J20yNbrHbYkzZGbPS7Hq84DRX4rng0sT-HUXTYzZmRtzneJEg8-KD6vIJi4cCr8x4GgspQl_nZzCvnQ8If3PMDiFoqWF5JXW6ZjrpZWO9w6KTtvJAv",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv94DTMLimuIhJSCxbRWjE9-zrgGFV3pPJJn6Gdt5z8qw4xGLbPyCSmfbkm7OXiWDTqVLV_KMGcYGDghaDnaAVLeooSukTi-ISm-NwZrbyYD_Mme7oF0i4BgDot0jbzE3aeBPa2jQSAjrGl3Rn7HAf1zmI875X5hPKxfOAie4JhY1ilZ259Ws5dm-16pZEVCON0qOqJyp1otWRLvkS1ik-E4viEB0ZAGANfwGEGCaFBFw6BP-5s-qQJwEFhcSkMOt_yoqo-Kh48eSl53aIy4wt9Wv5sgDt6dNgpg8i-ZZD9MJ8ZdNf-YShMvAhTf268TUaScyv3WIç",
        "https://hashcodejudge.withgoogle.com/download/blob/AMIfv97dgUsRkZX-sPN6ZjxVuupAVdZtpeLNfh2m1Y1brcUXLNq4SuwjqPA8Adl4FcNRewazJSiXfhQxjlgUNOnxlSF9hJxJdBzl2LIthcs2VBrD41rNUtd077k277McQLMFgwx1qPjvwnynXnUAZqE3F8XiTq9uOpAWSuMW1h8nbJwNCDcrH3-0ZPxW-3AGbozbJw6jWpCYuF2Gsq5Ato2ijJtI_hq9_7Oj37ddoFsYXOJnLO0toEK-hP4c9ItPQWm4SvrI3X2NPckkP15ImXsUhFXohgj-ZaudpG7he0X4oqpWoLAzJ3M0UyfMKHF5P9O1bLU-yi-8"
        ]

    d = Dataset(datasetURLs[0])

if __name__ == "__main__":
    main()