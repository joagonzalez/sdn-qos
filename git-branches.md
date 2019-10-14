# sdn-qos
sdn-qos

## Ver videos (drive)
Branches: Mergear finalment solo a una y comenzar a utilizar tags. Hoy en dia tenemos 2 principales y una tercera con feature experimental.

- cac-be-with-gui-topology-call-simulation-and-graphic-traffic-ovs-over-mn -- sipp simulation + cac + gui topology
- CAC_App_v1_refactor -- real time qos scripts and wireshark i/o
- cac-traffic-reporter-graph -- traffic reporter class que broadcastea con tshark/tcpdump data de simulator al backend y luego al frontend

```
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

```
# Show git branch name
force_color_prompt=yes
color_prompt=yes
parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
if [ "$color_prompt" = yes ]; then
 PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
else
```
