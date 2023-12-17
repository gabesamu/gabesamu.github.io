---
title: 'Basics of Hash Tables - Represented in C'
pubDate: 2023-08-01
description: 'Writings/notes on the basics of hash structures with example code in C.'
tags: ["hash-table", "data-structures", "C", "notes"]
---

## Overview

Just go read this: [Wikipedia](https://en.wikipedia.org/wiki/Hash_table#)

I considered writing up my own overview/intro, but everything I'd type would either
be the same or even less comprehensive than that page. It's the perfect surface level view of the hash table structure.
For ease I'll just include from that page the initial paragraphs giving a brief description.

>In computing, a hash table, also known as hash map, is a data structure that implements an associative array or dictionary. It is an .abstract data type that maps keys to values. A hash table uses a hash function to compute an index, also called a hash code, into an array of buckets or slots, from which the desired value can be found. During lookup, the key is hashed and the resulting hash indicates where the corresponding value is stored.
>
>Ideally, the hash function will assign each key to a unique bucket, but most hash table designs employ an imperfect hash function, which might cause hash collisions where the hash function generates the same index for more than one key. Such collisions are typically accommodated in some way.
>
>In a well-dimensioned hash table, the average time complexity for each lookup is independent of the number of elements stored in the table. Many hash table designs also allow arbitrary insertions and deletions of key–value pairs, at amortized constant average cost per > operation.

Below I'll be sharing a basic implementation in C and some notes on the code. I may also include links to other resources I have found helpful or interesting.

## Implementation
The implementation here will be using chaining to handle collisions. This means that each array location in the hash map will be another data structure storing potentially more than one piece of data. Specifically here I use a linked list for the chaining since it is the simplest implementation possible, and that is the goal here.


### Basic Structure of the data
```c
typedef struct Node{

    int key;
    int value;
    struct Node *next;

} Node;

typedef struct ArrayItem{

    Node *head;

} ArrayItem;


typedef struct {

    ArrayItem *buckets;
    int num_of_buckets;
    int num_of_elements;
    float max_load_factor;

} HashMap;

```

The necessary data is as simple as this. The `HashMap` struct is the main data structure that will be used to represent the hash table. It contains an array of `ArrayItem` structs. Each `ArrayItem` contains a pointer to the head of a linked list of `Node` structs. Each `Node` contains the key and value of the data being stored, as well as a pointer to the next `Node` in the linked list.

The `ArrayItem` struct is not actually necessary, but It is useful in case you want to store more informations about the list, such as the length or a pointer to the tail. Without is each array "bucket" would just contain a pointer to the head of the linked list.


### Initializing the HashMap
```c
HashMap* hashmap_create() {

    HashMap *hash_map = (HashMap*) malloc(sizeof(HashMap));

    if (hash_map == NULL) {
        return NULL;
    }

    hash_map->num_of_buckets = 128;
    hash_map->buckets = (ArrayItem*) calloc(hash_map->num_of_buckets, sizeof(ArrayItem));

    if (hash_map->buckets == NULL) {
        free(hash_map);
        return NULL;
    }

    hash_map->num_of_elements = 0;
    hash_map->max_load_factor = 1.0;

    return hash_map;

}

```

This function allocates the memory for the map and its array of data. I use calloc to allocate the array because I want to ensure the head pointer is NULL instead of arbitrary data.

I use 128 as the size of the array because it is a power of 2, which allows for fast hashing with bit operations instead of using modulo. It also makes resizing the array trivial since it can just be doubled. The downside to this is that if the hash function is not very good, there will be a lot of collisions. I may write a separate post on hash functions and their effects on hash structures, but for now I'll just include some links that I found insightful.

[Discussing the effects of using prime number size vs power of 2 size](https://stackoverflow.com/questions/1145217/why-should-hash-functions-use-a-prime-number-modulus)

I store a max_load_factor which is used to check if the array needs to be resized. I have it set to 1.0 because chaining can handle a higher load factor with less of a speed hit than the probing opproach.


### Functions for manipulating the HashMap
```c
void hashmap_put(HashMap* obj, int key, int value) {

    int index = key & (obj->num_of_buckets - 1);
    ArrayItem *bucket = &(obj->buckets[index]);

    Node *existing_node = findKey(bucket, key);

    if (existing_node != NULL) {
        existing_node->value = value;
        return;
    }

    Node *new_node = (Node*) malloc(sizeof(Node));

    if (new_node == NULL) {
        return NULL;
    }

    new_node->key = key;
    new_node->value = value;

    if (bucket->head == NULL) {
        new_node->next = NULL;
    }

    else {
        new_node->next = bucket->head;
    }

    bucket->head = new_node;
    obj->num_of_elements += 1;

    if ((1.0 * obj->num_of_elements) / obj->num_of_buckets >= obj->max_load_factor) {
        hashmap_rehash(obj);
    }

}

int hashmap_get(HashMap* obj, int key) {

    int index = key & (obj->num_of_buckets - 1);
    ArrayItem *bucket = &(obj->buckets[index]);
    Node *head = bucket->head;

    while ((head != NULL) && (head->key != key)) {
        head = head->next;
    }

    if (head == NULL) {
        return -1;
    }

    return head->value;
}

void hashmap_remove(HashMap* obj, int key) {

    int index = key & (obj->num_of_buckets - 1);
    ArrayItem *bucket = &(obj->buckets[index]);
    Node *head = bucket->head;

    if (head == NULL) {
        return NULL;
    }

    if (head->key == key) {
        bucket->head = head->next;
        free(head);
        return;
    }

    Node *prev = NULL;

    while ((head != NULL) && (head->key != key)) {
        prev = head;
        head = head->next;
    }

    if (head == NULL) {
        return;
    }

    prev->next = head->next;
    free(head);
}

```

These are the basic functions for manipulating the hash map. The `hashmap_put` function takes a key and value and stores them in the map. It first hashes the key to get the index of the array to store the data in. It then checks if there is already a node in the list with the same key. If there is, it just updates the value of that node. If not, it creates a new node and adds it to the head of the list.

The `hashmap_get` function takes a key and returns the value associated with that key. It first hashes the key to get the index of the array to search. It then iterates through the linked list at that index until it finds a node with the same key. If it reaches the end of the list without finding a node with the same key, it returns -1.

The `hashmap_remove` function takes a key and removes the node with that key from the map. It first hashes the key to get the index of the array to search. It then iterates through the linked list at that index until it finds a node with the same key. If it reaches the end of the list without finding a node with the same key, it does nothing. If it finds a node with the same key, it removes that node from the list and frees the memory.
