---
author: TRAN-THUONG Tien-Thinh et JEAN Aimé
title: Projet de programmation
subtitle: Séance 2 question 11
geometry: margin=2.3cm
---
# Affirmation
La puissance minimale pour couvrir un trajet dans le graphe $G$ est égale à la puissance minimale pour couvrir ce trajet dans l'arbre $A_{min}$

# Notation
$A$ est un arbre couvrant de $G$  
$A_{min}$ est l'arbre couvrant minimal de $G$  
$u, v, i_k$ des nœuds de $G$  
$t_G(u, v)$ un trajet dans $G$ de $u$ à $v$  
$t_A(u, v)$ l'unique trajet (car $A$ est un arbre) dans $A$ de u à v  
On pourra écrire de manière équivalente $t_G(u, v)$ et $i_1^G-i_2^G-...-i_{n-1}^G-i_n^G$ avec $u=i_1^G\ et\ v=i_n^G$   
$p(t_G(u, v))$ la puissance minimale du trajet $t_G(u, v)$  
$p(A)$ est la somme des puissances de l'arbre $A$

# Démonstration par l'absurde
Soit $G$ un graphe  
Soit $A_{min}$ un arbre couvrant minimal de $G$  
Soit $u, v$ des nœuds de $G$  

Par l'absurde, supposons qu'il existe un trajet $t_G(u, v)$ tel que $p(t_G(u, v)) < p(t_{A_{min}}(u, v))$

Notons : $t_{A_{min}}(u, v) = i_1^{A_{min}}-...-i_n^{A_{min}}$  
Alors $\exists\ k \in [1, n-1]\ tq\ p(i_k^{A_{min}}-i_{k+1}^{A_{min}}) = p(t_{A_{min}}(u, v))$  

En rompant l'arête $i_k^{A_{min}}-i_{k+1}^{A_{min}}$ dans l'arbre $A_{min}$, on obtient 2 arbres. Le nœud $u$ est dans un arbre et $v$ est dans l'autre car l'unique chemin les reliant dans $A_{min}$ n'existe plus.  
Notons $A_u$ l'arbre contenant $u$ et $A_v$ l'arbre contenant $v$.  

Notons :  $t_G(u, v) = i_1^G-...-i_m^G$  avec $u=i_1^G \in A_u$ et $v=i_m^G \in A_v$   
Donc $\exists\ l \in [1, m], i_l^G \in A_u\ et\  i_{l+1}^G \in A_v$  

Remarque : 
$$
\begin{aligned}
p(i_l^G-i_{l+1}^G) & \leq p(t_G(u, v)) \\
& < p(t_{A_{min}}(u, v))\ par\ hypothèse \\
& = p(i_k^{A_{min}}-i_{k+1}^{A_{min}})
\end{aligned}
$$  

En ajoutant l'arête $i_l^G-i_{l+1}^G$, on relie les arbres $A_u$ et $A_v$ pour former un arbre couvrant $A'$ de G. De sorte que : 
$$
\begin{aligned}
p(A') & = p(A_{min}) + p(i_l^G-i_{l+1}^G) - p(i_k^{A_{min}}-i_{k+1}^{A_{min}}) \\
& < p(A_{min})
\end{aligned}
$$  
Ce qui est **absurde** car par hypothèse $A_{min}$ est l'arbre couvrant minimal. On a donc démontré le l'affirmation.

