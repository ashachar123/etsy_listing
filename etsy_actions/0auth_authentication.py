from etsyv3.util.auth import AuthHelper


code_verifier = "vvkdljkejllufrvbhgeiegrnvufrhvrffnkvcknjvfid"
code_challenge = AuthHelper._generate_challenge(code_verifier)
code_challenge_expected = "DSWlW2Abh-cf8CeLL8-g3hQ2WQyYdKyiu83u_s7nRhI"
auth = AuthHelper("xuaafzb74heexv0ige5doz1r","https://eolvm1ot8icqxm3.m.pipedream.net", scopes=["transactions_r","transactions_w", "listings_w"],
                  state="superstate", code_verifier="secretfuck")
auth.set_authorisation_code(code="TDc2xl6w4VRMfmWIOTHYprBvPyKNt6keNnCQAhyowUz3PHKDAbUiGqZp7iOlQUtnyGcp7FyTQU_VrK9K1bcau32i3HQvgv0vM5wy", state="superstate")
print(auth.get_access_token())

#oauthtoken = 7pOriUThmJnPa_Eoo28vM6TKe5cA57ECUeVqIE8grxHzokCRecB6tiz20vx-V7cIxo4hHMN67zB2fULul-zWcp0tMbgVZ0VTCYyx
# {'access_token': '882842516.FKXlfw8oWt9aTee-IqxHvRZCHwZZAKU1M6hi38dSv615GIbIxZnoTnwAV1PqV_6lXO1SazyNIr9_gRPLu_Zuat5dzu', 'token_type': 'Bearer', 'expires_in': 3600, 'refresh_token': '882842516.kSA-FdLo8B_n8pNMipgGuBPsI1L2GjYw3wKm4x6NgKh9wa2GmCDeszDVHvl-h_3jDVIy3NhbD6UCmW9nTs3i5KTSkn', 'expires_at': 1705697557.4447832}
