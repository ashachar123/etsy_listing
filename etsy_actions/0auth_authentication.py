from etsyv3.util.auth import AuthHelper


code_verifier = "vvkdljkejllufrvbhgeiegrnvufrhvrffnkvcknjvfid"
code_challenge = AuthHelper._generate_challenge(code_verifier)
code_challenge_expected = "DSWlW2Abh-cf8CeLL8-g3hQ2WQyYdKyiu83u_s7nRhI"
auth = AuthHelper("xuaafzb74heexv0ige5doz1r","https://", scopes=["transactions_r","transactions_w", "listings_w"],
                  state="superstate", code_verifier="secretfuck")
auth.set_authorisation_code(code="", state="superstate")
print(auth.get_access_token())

