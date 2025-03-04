# python_pair_programming

## How to pair programming with us

install Python 3.10 on your machine

    add command here

install pre-commit

    add command here

install pipenv

    add command here

create a pipenv shell with the Pipfile on this project

    add command here

lock dependencies

    add command here

install the requirements

    add command here

## How to start a new kata

Please create a new branch of this project including the date of the session

    git checkout -b pair_session_19.05.2023

Start a new section on this file using the last section as template
introduce name, link, description to the problem you want to solve and
a happy path test with examples

Disscuss the solution with your colleagues

When you get to a common approach to the problem, start a new file .py with the name of the problem

First write the tests!!

Code the solution as a function so it could be easily tested

When you finish the sesion, create a PR for at least one contributor to review

Please lint your code with pre-commit before creating the PR

    pre-commit run --all

Have fun!

## How to collaborate

We have an utilities.py file with common stuff we can use

Please document your functions you think could be usefull for others on that file

## Climbing the leaderboard

<https://www.hackerrank.com/challenges/climbing-the-leaderboard/problem>

An arcade game player wants to climb to the top of the leaderboard and track their ranking. The game uses Dense Ranking, so its leaderboard works like this:

- The player with the highest score is ranked number 1 on the leaderboard.
- Players who have equal scores receive the same ranking number, and the next player(s) receive
  the immediately following ranking number.

Example

    ranked = [100, 90, 90, 80]
    player = [70, 80, 105]

    result = [4,3,1]

## Multiples of 3 or 5

<https://www.codewars.com/kata/514b92a657cdc65150000006>

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Finish the solution so that it returns the sum of all the multiples of 3 or 5 below the number passed in. Additionally, if the number is negative, return 0 (for languages that do have them).

Note: If the number is a multiple of both 3 and 5, only count it once.

Example

    number = 5 return 3
    number = 15 returns 45
    number = -5 returns 0

## Spinning Words

<https://www.codewars.com/kata/5264d2b162488dc400000001>

Write a function that takes in a string of one or more words, and returns the same string, but with all five or more letter words reversed (Just like the name of this Kata). Strings passed in will consist of only letters and spaces. Spaces will be included only when more than one word is present.

Example

    spinWords( "Hey fellow warriors" ) => returns "Hey wollef sroirraw"
    spinWords( "This is a test") => returns "This is a test"
    spinWords( "This is another test" )=> returns "This is rehtona test"

## Find the odd int

Session: 20-05-2023

Contributors: madtyn, mateocpdev, pedrolp85

<https://www.codewars.com/kata/54da5a58ea159efa38000836>

Given an array of integers, find the one that appears an odd number of times.

There will always be only one integer that appears an odd number of times.

Example

        [7] should return 7, because it occurs 1 time (which is odd).
        [0] should return 0, because it occurs 1 time (which is odd).
        [1,1,2] should return 2, because it occurs 1 time (which is odd).
        [0,1,0,1,0] should return 0, because it occurs 3 times (which is odd).
        [1,2,2,3,3,3,4,3,3,3,2,2,1] should return 4, because it appears 1 time (which is odd).


## read workloads

Sean los fichero estáticos .yml en static_files/OCPClusterX.yml representaciones de workloads 
de K8s

Lee los ficheros en la estructura que prefieras y hay que satisfacer los tests en read_workloads.py

Nota:

    Cada cluster puede tener un número indeterminado de nodos
    Cada nodo es único, y suma para la adición de recursos
    Un nodo puede tener o no la línea node_labels

    Los namespaces son estructuras lógicas que se replican en todos los nodos de k8s
    Su utilidad es delimitar el acceso a recursos de las aplicaciones
    En los ficheros de test cada ns tiene un nombre diferente

    Al similar ocurre con los pods, 2 pods con el mismo nombre pueden existir en ns diferentes

    Labels:

        Las etiquetas se usan para seleccionar recursos en kubernetes
        Sin embargo, son estructuras del tipo clave:valor, con sus limitaciones

        No podemos tener 2 valores diferentes para una misma clave dentro de un mismo dominio 
        de colisión

        Para ello se establece una precedencia en sentido descendente

        Consideramos "iguales" 2 claves que compartan cluster, nodo, ns o pod
        Viendo el ejemplo del cluster 1:

        Para el Pod: pod_1
        label_tier: pod1

        Para el Pod: pod_2
        label_tier: pod_2

        Las etiquetas del cluster deben contener ambos valores para esa clave
        Los tests siempre nos pedirán los valores finales, con la precedencia aplicada

        Almacenar los valores intermedios no es obligatorio



    test_get_cluster_name(input_file, expected_cluster_name)
        devuelve el cluster_name
    
    test_get_cpu_count(input_file, expected_cpu_count)
        devuelve la suma de las cpu de los nodos que forman el cluster

    test_get_mem_count(input_file, expected_mem_count)
        devuelve la suma de GB de los nodos que forman el cluster

    test_get_all_nodes()
        devuelve todos los nodos del cluster

    test_get_all_ns()
        devuelve todos los ns del cluster

    test_get_all_pods()
        devuelve todos los pods del cluster        

    test_get_ns_by_node()
        devuelve los ns de los nodos que macheen con la regex 

    test_get_pods_by_ns()
        devuelve los ns de los nodos que macheen con la regex 






## problem name

a link to the problem

Session: day of the session

Contributors: name or github of contributors

This is the explanation of the problem
    - We could use bulletpoints

Example

    this the happy path test case
