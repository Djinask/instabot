from tqdm import tqdm
from collections import Counter


def like_and_follow_users_media_n_liker(self, users, pivot=2, last_n_media=2):
    nlike = int(pivot)
    seen = set()
    for username in tqdm(users, desc="Getting Users"):
        alllikers = list()
        bestfan= list()
        medias = self.get_user_medias(username, filtration=False)
        if medias:
            for media in tqdm(medias, desc="Getting medias"):
                likers = self.get_media_likers(media)
                alllikers = alllikers+likers
        counter = Counter(alllikers)
        print('Found %i unique likers' % (len(counter)))
        most_liker = dict(counter.most_common())  # Create a dictionary {[(pk), nlike],..}
        ordered_liker = dict([(value, [key for key, v in most_liker.items() \
                                               if v == value]) for value in set(
                    most_liker.values())])  # switch the dictionary {[nlike, (pk,'username')],..}
        self.logger.info('Range %i to %i' % (nlike, len(ordered_liker)))
        self.logger.info('Start to like and follow')
        for item in tqdm(range(len(ordered_liker), nlike-1, -1), desc='Liking and following'): # use the pivot for filter the min like parameter
            if item in ordered_liker:
                for user in ordered_liker[item]:
                    tmp = user
                    if tmp not in seen:
                        self.logger.info('Fun found %s' % tmp)
                        seen.add(tmp)
                        bestfan.append(user)
                        self.like_user(user, last_n_media)
                        self.follow(user)
