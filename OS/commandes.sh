#TP5
#Question1
cd ~
mkdir files
sudo cp /etc/passwd /etc/shadow /etc/group ~/files
#Methode 1: les commandes

groupadd Etudiants
groupadd Enseignants 
groupadd Administration
useradd -m -d /home/Etudiants/Mohamed -g 1001 -s /bin/bash Mohamed
useradd -m -d /home/Etudiants/Fatima -g 1001 -s /bin/bash Fatima
useradd -m -d /home/Enseignants/Brahim -g Enseignants -s /bin/bash Brahim
useradd -m -d /home/Enseignants/Youness -g Enseignants -s /bin/bash Youness
# -d pour specifier le rep personel et -m pour le creer
#A revoir structure /etc/passwd /etc/shadow /etc/group
#Question 3
usermod -c "Brahim laaroussi" Brahim
cat /etc/passwd |egrep "^(Brahim|Mohamed|Fatima|Youness):"
#Question 4 
passwd Fatima
#Question 5
cat etc/shadow |egrep "^(Brahim|Mohamed|Fatima|Youness):"
# ! pas de mot de pass 
#pour verouiller un user
passwd Brahim -l
#pour deverouiller un user
passwd Brahim -u
#Question 6
# le champ 4 -n represent durre min pour changer le mdp : nombre de jours avant lesquels le mot de passe ne peut pas être changé (0 : il peut être changé n’importe quand).
passwd Brahim -n 15 
##champ 5 ie -x 28 apres 28 jours l'utilisateur est obligé de changé le mdp 
passwd Brahim -x 28
passwd Brahim -w 5
passwd Brahim -i 3
#Question 5
passwd -u Youness
#Question 6
passwd -x 0 Youness
passwd -e Yoness
## Question 7
# Changement dans /etc/login.defs




