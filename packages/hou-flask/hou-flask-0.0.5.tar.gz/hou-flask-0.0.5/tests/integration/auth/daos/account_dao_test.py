class GetUsernameTest:
    def test_when_id_exists__returns_username(self):
        account = AccountFactory.build()
        username = AccountDAO.get_username(account.id)
        assert username.account_id == account.id
        assert username.username == account.email

    def test_when_id_not_exists__raises_not_found_exception(self):
        with pytest.raises(SQLNotFoundException):
            AccountDAO.get_username(uuid4())


class GetUserNamesTest:
    def test_when_name_filter_empty__returns_all_usernames_and_ids(self):
        accounts = AccountFactory.build_batch(3)
        expected_usernames = {Username(a.id, a.email) for a in accounts}
        resp = AccountDAO.get_usernames("", 0, 1000)
        assert expected_usernames.issubset(set(resp))

    @pytest.mark.parametrize(("name_filter",), [("%",), ("e%",), ("%t",), ("e%t",)])
    def test_when_percentage_sign_in_name_filter__finds_all_usernames_with_percentage_sign(
        self, name_filter
    ):
        AccountFactory.build_batch(2)
        target_account = AccountFactory(email="some%thing")
        expected_response = [Username(target_account.id, target_account.email)]

        resp = AccountDAO.get_usernames(name_filter, 0, 1000)
        assert expected_response == resp

    def test_when_name_exact_match__returns_username(self):
        account = AccountFactory()

        resp = AccountDAO.get_usernames(account.email, 0, 1000)
        assert [Username(account.id, account.email)] == resp

    def test_when_no_name_matches__returns_empty(self):
        AccountFactory.build_batch(3)
        name_filter = random_string()
        resp = AccountDAO.get_usernames(name_filter, 0, 1000)
        assert resp == []

    def test_when_multiple_pages__returns_distinct_case_insensitive_sorted_batches(
        self
    ):
        AccountFactory.build_batch(10)

        resp1 = AccountDAO.get_usernames("", 0, 5)
        resp2 = AccountDAO.get_usernames("", 1, 5)

        # ensure distinct batches
        assert set(resp1).isdisjoint(set(resp2))
        usernames1 = [u.username.lower() for u in resp1]
        usernames2 = [u.username.lower() for u in resp2]
        min_in_set2 = min(usernames2)
        max_in_set1 = max(usernames1)

        # Ensure every username in set 2 is greater
        # than every name in set 1 and vice versa
        assert all(max_in_set1 <= username for username in usernames2)
        assert all(min_in_set2 >= username for username in usernames1)


class GetAccountInfoTest:
    def test_when_valid__returns_account(self):
        account = AccountFactory()

        resp = AccountDAO.get_account_info(account.id)

        assert resp == Account(username=account.email, id=account.id)

    def test_when_not_found__raises_sqlobject_not_found(self):
        with pytest.raises(SQLNotFoundException):
            AccountDAO.get_account_info(uuid4())
