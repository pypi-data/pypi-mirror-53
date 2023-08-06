# AWS SSH Proxy

An ssh `ProxyCommand` utility that allows users to ssh by using the AWS EC2
instance names instead of having to remember the random public DNS names used by
AWS for each instance.

The idea is that AWS EC2 instance names used will have a more memorable name
that users will be remember and share. With this utility it is now possible to
use these names as functional host names recognized by ssh and any other command
that relies on ssh:

 - ssh
 - scp
 - rsync
 - sftp
 - git
 - FUSE
 - Gnome's VFS

 
# Installation

To install it run:

```
pip install aws-ssh-proxy
```

Then update your ssh configuration `~/.ssh/config` with:

```
Host *
    ProxyCommand aws-ssh-proxy %h %p
```

You might want to update your ssh configuration with a more specific rule.
See the rest of the document for a more elaborate setup.

# How it works

In order to use this command with ssh it is required that the argument
`ProxyCommand` is used. This will instruct ssh to request at the program passed
to establish the connection to the remote host.

This program will then search the list of AWS EC2 instances that are running for
one who's name matches the hostname passed in parameter.

For the program to work you will need to have your environment setup in order to
work with AWS. This usually means that you have the following environment
variables defined:

 - `AWS_ACCESS_KEY_ID`
 - `AWS_SECRET_ACCESS_KEY`

# SSH Configuration

Modify your ssh configuration (`~/.ssh/config`) so that `ProxyCommand` uses
`aws-ssh-proxy`.

There are multiple ways to achieve this. In theory the following configuration
should work:

```
Host *
    ProxyCommand aws-ssh-proxy %h %p
```

Although the previous configuration will work it will probably create problems.
It is suggested that you read the next section and setup your own configuration.


## Advanced usage

It is best is you restrict the usage to `aws-ssh-proxy` to only the hosts that are
in AWS. You can achieve this by simply tricking ssh into believing that all
your hosts are under the same domain.

The idea is to pretend that you own a given domain, for instance `.aws` and to
build an ssh rule that matches that domain. You do not need to own the domain
nor to have your server names with that domain.

All that you need is to build a rule so that ssh can match connections to there
and to instruct it what to do:

```
Host *.aws                                         # Pretend that our servers all end with .aws
    ProxyCommand aws-ssh-proxy --suffix .aws %h %p # Tell ssh to use aws-ssh-proxy to establish the connection
```

Wit this we can now have the following host names in AWS:

  - mysql-dev
  - webserver-dev

And we can ssh to them with `ssh webserver-dev.aws` and `ssh mysql-dev.aws`. The
`.aws` suffix is used only for telling which ssh configuration section to
trigger.

The suffix can be anything, in fact it can be even a prefix and it would work
perfectly well too:

```
Host aws-*
    ProxyCommand aws-ssh-proxy --prefix aws- %h %p
```

# Tweaks

You can customize your ssh connections to your liking. It is possible to combine
this with other ssh rules.

## Prefiling the remote username

If your AWS EC2 instances are all of the same OS or if most are of the same OS
you can set the default user name, for instance Ubuntu servers use the username
`ubuntu` while AWS EC2's Amazon Linux 2 use `ec2-user`.

You can combine the rules with the `User` directive:

```
Host *.aws                                          # Pretend that our servers all end with .aws
    User          ec2-user                          # Default username to use
    ProxyCommand  aws-ssh-proxy --suffix .aws %h %p # Tell ssh to use aws-ssh-proxy to establish the connection
```
Your ssh connection will then default to be done with the remote use `ec2-user`
and if you have a server with a different user you can still change it by
providing the user name in the command line:

```
ssh -l ubuntu ubuntu-box.aws
ssh ubuntu@ubuntu-box.aws
```

## Avoiding: Remote host identification changed

**NOTE: Be aware that ignoring the server fingerprint can be a security risk!**

AWS EC2 hosts are ephemeral and can be recreated at any time. Since `aws-ssh-proxy`
avoids that users need to remember that DNS public names and that they can rely
on common names it is possible that names will give ssh errors as EC2 instances
are replaced and the name remains unchanged.

A typical ssh error when connecting to a host that has changed:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd:ee:ff.
Please contact your system administrator.
Add correct host key in ~/.ssh/known_hosts to get rid of this message.
Offending key in ~/.ssh/known_hosts:1
RSA host key for 10.11.12.13 has changed and you have requested strict checking.
Host key verification failed.
```

In order to avoid these errors it is possible to disable `StrictHostKeyChecking`.
Note that this will come at its own security risk. If you're not limiting this
your own AWS EC2 servers you can be under a lot of risk!

The configuration can be done for all hosts.

```
Host *.aws
    ProxyCommand            aws-ssh-proxy --suffix .aws %h %p
    StrictHostKeyChecking   no
    UserKnownHostsFile      /dev/null
```

**NOTE: Be aware that ignoring the server fingerprint can be a security risk!**

## Corporate firewall issues; http(s) proxy to the rescue

If you're behind a corporate firewall that prevents you from using ssh directly to AWS EC2 hosts you can try to use your corporate http(s) to the rescue.

```
Host *.aws
    User          ec2-user
    ProxyCommand  aws-ssh-proxy --suffix .aws --auto-proxy %h %p
```

With `--auto-proxy` the environment variables for the proxy will be used in order to establish a connection via the proxy.

This is the equivalent of running:

```
nc -X connect -x $proxy_host:$proxy_port %h %p
```

**NOTE: You need netcat BSD to be installed for this to work.**
