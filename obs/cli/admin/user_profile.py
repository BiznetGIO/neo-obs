import click

from obs.libs import user as user_lib


def prompt_user_profile():
    """Prompt user interactively for data"""
    user_profile = user_lib.UserProfile()
    options = [
        ("userId", "User ID"),
        ("groupId", "Group ID"),
        ("userType", "User Type"),
        ("fullName", "Full Name"),
        ("emailAddr", "Email"),
        ("address1", "Address"),
        ("city", "City"),
        ("state", "State"),
        ("zip", "Zip"),
        ("country", "Country"),
        ("phone", "Phone"),
        ("website", "Website"),
        ("active", "Active"),
        ("ldapEnabled", "LDAP Enabled"),
    ]
    try:
        while True:
            click.secho("Put in new values or accept defaults.")
            for option in options:
                prompt = option[1]
                val = getattr(user_profile, option[0])
                if val not in (None, ""):
                    prompt += f" [{val}]"

                if len(option) >= 3:
                    click.secho(f"\n{option[2]}")

                val = input(prompt + ": ")
                # only set new value if user provide one
                if val != "":
                    setattr(user_profile, option[0], val)

            val = input("\nSave settings? [y/N] ")
            if val.lower().startswith("y"):
                break

            val = input("Retry entry? [Y/n] ")
            if val.lower().startswith("n"):
                raise EOFError()

        data = user_profile.dump(options, user_profile)
        return data

    except (EOFError, KeyboardInterrupt):
        click.secho("\nData enty aborted.", fg="yellow", bold=True, err=True)
        return
