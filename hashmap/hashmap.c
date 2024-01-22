#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STARTING_BUCKETS 8
#define MAX_KEY_SIZE 20

typedef struct LLNode {
  struct LLNode *next;
  const char *key;
  void *value;
} LLNode;

LLNode *LLNode_new(const char *key, void *value) {
  LLNode* llnode = malloc(sizeof(LLNode));
  printf("create LLN with key %s\n", key);
  llnode->key = strdup(key);
  llnode->value = value;
  llnode->next = NULL;
  return llnode;
}

typedef struct Hashmap {
  LLNode **buckets;
} Hashmap;

int get_bucket(const char* str) {
  unsigned long hash = 5381;
  int c;

  while ((c = *str++)) {
    hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
  }

  return hash % STARTING_BUCKETS;
}

Hashmap *Hashmap_new(void) {
  Hashmap* hm  = malloc(sizeof(Hashmap));
  hm->buckets = malloc(STARTING_BUCKETS * sizeof(LLNode*));
  for (int i = 0; i < STARTING_BUCKETS; i++) {
    hm->buckets[i] = NULL;
  }
  return hm;
}

void Hashmap_free(Hashmap *hm) {
  // TODO free linked list
  free(hm);
}

void Hashmap_set(Hashmap *hm, const char *key, void *value) {
  int bucket = get_bucket(key);
  LLNode *lln = hm->buckets[bucket];
  LLNode *prev = NULL;
  while (lln != NULL) {
    printf("bucket %d has lln with key '%s'\n", bucket, lln->key);
    if (strcmp(lln->key, key) == 0) {
      lln->value = value;
      return;
    }
    prev = lln;
    lln = lln->next;
  }
  if (prev == NULL) {
    hm->buckets[bucket] = LLNode_new(key, value);
  } else {
    prev->next = LLNode_new(key, value);
  }
}

void *Hashmap_get(Hashmap *hm, const char *key) {
  int bucket = get_bucket(key);
  LLNode *lln = hm->buckets[bucket];
  while (lln != NULL) {
    if (strcmp(lln->key, key) == 0) {
      return lln->value;
    }
    lln = lln->next;
  }
  return NULL;
}

void Hashmap_delete(Hashmap *hm, const char *key) {
  int bucket = get_bucket(key);
  LLNode *lln = hm->buckets[bucket];
  LLNode *prev = NULL;
  while (lln != NULL) {
    if (strcmp(lln->key, key) == 0) {
      if (prev != NULL && lln->next != NULL) {
        prev->next = lln->next;
      } else if (prev != NULL && lln->next == NULL) {
        prev->next = NULL;
      } else if (prev == NULL && lln->next != NULL) {
        hm->buckets[bucket] = lln->next;
      } else if (prev == NULL && lln->next == NULL) {
        hm->buckets[bucket] = NULL;
      }
      return;
    }
    prev = lln;
    lln = lln->next;
  }
}

int main() {
  Hashmap *h = Hashmap_new();

  // basic get/set functionality
  int a = 5;
  float b = 7.2;
  Hashmap_set(h, "item a", &a);
  Hashmap_set(h, "item b", &b);
  assert(Hashmap_get(h, "item a") == &a);
  assert(Hashmap_get(h, "item b") == &b);

  // using the same key should override the previous value
  int c = 20;
  Hashmap_set(h, "item a", &c);
  assert(Hashmap_get(h, "item a") == &c);

  // basic delete functionality
  Hashmap_delete(h, "item a");
  assert(Hashmap_get(h, "item a") == NULL);

  // handle collisions correctly
  // note: this doesn't necessarily test expansion
  int i, n = STARTING_BUCKETS * 10, ns[n];
  char key[MAX_KEY_SIZE];
  for (i = 0; i < n; i++) {
    ns[i] = i;
    sprintf(key, "item %d", i);
    Hashmap_set(h, key, &ns[i]);
  }
  for (i = 0; i < n; i++) {
    sprintf(key, "item %d", i);
    assert(Hashmap_get(h, key) == &ns[i]);
  }

  Hashmap_free(h);
  /*
     stretch goals:
     - expand the underlying array if we start to get a lot of collisions
     - support non-string keys
     - try different hash functions
     - switch from chaining to open addressing
     - use a sophisticated rehashing scheme to avoid clustered collisions
     - implement some features from Python dicts, such as reducing space use,
     maintaing key ordering etc. see https://www.youtube.com/watch?v=npw4s1QTmPg
     for ideas
     */
  printf("ok\n");
}
