import asyncio

from library import get_user

loop = asyncio.get_event_loop()
data_standard = loop.run_until_complete(get_user('Arita', 'osu'))
data_taiko = loop.run_until_complete(get_user('Arita', 'taiko'))
# data_catch = loop.run_until_complete(get_user('Arita', 'catch'))
data_mania = loop.run_until_complete(get_user('Arita', 'mania'))
loop.close()


class TestClass:
    def test_osu_standard_data(self):
        assert data_standard.user_id == 7109858
        assert data_standard.username == 'Arita'
        assert data_standard.count300 > 0
        assert data_standard.count100 > 0
        assert data_standard.count50 > 0
        assert data_standard.playcount > 0
        assert data_standard.ranked_score > 0
        assert data_standard.total_score > 0
        assert data_standard.pp_rank > 0
        assert data_standard.level > 0
        assert data_standard.pp_raw > 0
        assert data_standard.total_seconds_played > 0
        assert data_standard.accuracy > 0
        assert data_standard.count_rank_ssh >= 0
        assert data_standard.count_rank_ss >= 0
        assert data_standard.count_rank_sh >= 0
        assert data_standard.count_rank_s >= 0
        assert data_standard.count_rank_a >= 0
        assert data_standard.country == 'AU'
        assert data_standard.pp_country_rank > 1

    def test_osu_taiko_data(self):
        assert data_taiko.user_id == 7109858
        assert data_taiko.username == 'Arita'
        assert data_taiko.count300 > 0
        assert data_taiko.count100 > 0
        assert data_taiko.count50 == 0
        assert data_taiko.playcount > 0
        assert data_taiko.ranked_score > 0
        assert data_taiko.total_score > 0
        assert data_taiko.pp_rank > 0
        assert data_taiko.level > 0
        assert data_taiko.pp_raw > 0
        assert data_taiko.total_seconds_played > 0
        assert data_taiko.accuracy > 0
        assert data_taiko.count_rank_ssh >= 0
        assert data_taiko.count_rank_ss >= 0
        assert data_taiko.count_rank_sh >= 0
        assert data_taiko.count_rank_s >= 0
        assert data_taiko.count_rank_a >= 0
        assert data_taiko.country == 'AU'
        assert data_taiko.pp_country_rank > 1

    def test_osu_mania_data(self):
        assert data_mania.user_id == 7109858
        assert data_mania.username == 'Arita'
        assert data_mania.count300 > 0
        assert data_mania.count100 > 0
        assert data_mania.count50 > 0
        assert data_mania.playcount > 0
        assert data_mania.ranked_score > 0
        assert data_mania.total_score > 0
        assert data_mania.pp_rank > 0
        assert data_mania.level > 0
        assert data_mania.pp_raw > 0
        assert data_mania.total_seconds_played > 0
        assert data_mania.accuracy > 0
        assert data_mania.count_rank_ssh >= 0
        assert data_mania.count_rank_ss >= 0
        assert data_mania.count_rank_sh >= 0
        assert data_mania.count_rank_s >= 0
        assert data_mania.count_rank_a >= 0
        assert data_mania.country == 'AU'
        assert data_mania.pp_country_rank > 1
