Release History
===============

0.7.0
-----

- Support SMC 6.6
- Add validate flag to all rule creation parameters and update parameters. Validate=False will circumvent validating
  the inspection policy during rule creation, making add operations faster when bulk loading rules
- SwitchPhysicalInterface implemented
- VPNProfile implemented
- VPN Mobile Gateways for Policy VPN
- Set default retries parameter on ActiveDirectoryServer to 3 retries
- Configurable gateway profile for ExternalGateway
- Geolocation objects (SMC 6.6)
- Update of docs for smc-python-monitoring
- SNMPAgent modified to accommodate SMC >= 6.5.1 requiring snmp_user_name field during creation
- Support ClientProtectionCA for compatibility with all >= 6.5.x versions
 
