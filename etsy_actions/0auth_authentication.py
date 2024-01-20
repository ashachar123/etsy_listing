from etsyv3.util.auth import AuthHelper


code_verifier = ""
code_challenge = AuthHelper._generate_challenge(code_verifier)
code_challenge_expected = ""
auth = AuthHelper("","", scopes=["transactions_r","transactions_w", "listings_w"],
                  state="superstate", code_verifier="secretfuck")
auth.set_authorisation_code(code="", state="superstate")
print(auth.get_access_token())
