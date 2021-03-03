# When biological viruses lead to infected computers

Cross-Secrecy ltd. is a small tech company. To reduce costs, management decided
to buy off old Vista computers from a shady storage depot.  Because of the huge
amount of problems with these office computers, the IT administrators have worked
overtime since ever.

To make their life easier, the administrators decided to develop an _agile_
web panel that every worker can file issues on. Issues added to the panel can
contain sensitive information. Therefore, read access to the panel is
granted to administrators only. However, anyone that is part of the same network can
add new issues using an _issue-client_.

Because of an ongoing pandemic, most workers started to work from home. To
guarantee that workers can still file new issues, the administrators decided to make
this functionality accessible from the internet.

The company also runs a chat server that workers can use for _lean_
communication. The administrators decided to incorporate the chat server into
their web panel and allow workers to _involve_ administrators into their group
chats whenever there is a technical problem they cannot solve.

You were hired as a white hat to evaluate the security of Cross-Secrecy's
IT-network. Convinced of their secure implementation, the administrators
happily shared the code of their web panel with you.  Prove to the
administrators that their solution is not secured against XSS attacks.
