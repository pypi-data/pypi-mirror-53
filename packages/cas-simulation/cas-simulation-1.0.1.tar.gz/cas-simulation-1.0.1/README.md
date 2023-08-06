# cas-simulation

A way to simulate a web browser visiting a service authenticated by
[CAS](https://en.wikipedia.org/wiki/Central_Authentication_Service) and
proceeding through the authentication.

Originally developed to facilitate authenticated service checks in Nagios.

# `check_cas_sp`

`cas_simulation` object instances are created using the included `check_cas_sp`
script, intended to be called from Nagios

The simulation will follow redirects from a starting URL (typically a service
provider like https://myportal.example.edu) until it reaches a form that it
believes is a CAS authentication page (at least the one presented by the
JASIG/Apereo implementation).  It will then submit the form using the
credentials provided. It will follow redirects and submit forms (e.g. "Click
here to continue" javascript alternatives) until it receives a 200 OK page
without a form, or the form contains an `id=` or `name=` attribute matching
argument provided to the `--form`.

The final landing page is searched for an expected pattern using
`--expression`.  If it matches, the script returns 0 which corresponds to a OK
in Nagios API.  Otherwise it returns 2 for CRITICAL

Optionally, the `check_cas_sp` will also fetch and check an expression against
a URL that is only expected to be available after authentication.  This would
simulate clicking a link on a portal after logging in.

## Gotchas

Notably, the `--verbose` option stupidly assumes it can write to
`/var/log/nagios`

## Examples

`check_cas_sp --help`

List all current command line options


```
check_cas_sp \
    --url https://fee-portal.csusb.edu/auth/shibboleth" \
    --expression "Fines .{1,30}for Joe Coyote" \
    -w 5.0 \
    --post-auth-check https://fee-portal.csusb.edu/fines/alma "Balance [Dd]ue" \
    --credentials "/etc/cas/joe-creds.json" \
```

Authenticate fee-portal.csusb.edu using the credentials in
/etc/cas/joe-creds.json.  The post authentication redirect contains "Fines and
fees for Joe Coyote" and should match the regular expression given.

After that check, also check a url that requires an authenticated active
session. In this case, a check for the Alma library fees that should contain
the text "Balance Due". Return WARNING if the authentication takes more than 5
seconds.  (It probably *should* be `--post-auth-url` and
`--post-auth-expression` instead of being combined like it is.)


```
check_cas_sp \
    --url https://my.csusb.edu \
    --expression 'Signed in as Joe Coyote<div .{1,30}>Tap to sign out' \
    -w 10 \
    --form '/default/kurogo_module_search/search' \
    --credentials credentails.json
```

Authenticate to my.csusb.edu and expect a name next to a "Tap to sign out"
after authentication.  Do not proceed past the form with the name or id of
'/default/kurogo_module_search/search' Typically, the simulation will submit
any forms it encounters, assuming they are "Click here to continue" type forms)


## Examples Nagios command objects

```
define command {
        command_name    check-cas-sp
        command_line    /opt/virtualenv/cas-simulation/bin/python $USER2$/check_cas_sp --url '$ARG1$' --expression '$ARG2$' $ARG3$ --verbose
}
```

```
define command {
        command_name    check-cas-sp-post-auth
        command_line    /opt/virtualenv/cas-simulation/bin/python $USER2$/check_cas_sp --url '$ARG1$' --expresison '$ARG2$' $ARG3$ --post-auth-check '$ARG4$' '$ARG5$' --verbose
}
```



