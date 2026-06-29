#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <time.h>

typedef struct {
    int row;
    int col;
} Pos;

typedef enum {
    FICTION,
    SCIENCE,
    FANTASY,
    HISTORY
} GENRE;

typedef struct {
    char* title;
    char* author;
    int pages;
    int year;
    GENRE type;     
    Pos position;
} Book;



Book* createBook(char* title, char* author, int pages, int year, GENRE type, Pos position) {
    Book* b = (Book*)malloc(sizeof(Book));
    if (!b) {fprintf(stderr, "Memory allocation failed\n"); return NULL;}

    b->title = title;
    b->author = author;
    b->pages = pages;
    b->year = year;
    b->type = type;
    b->position = position;
    return b;
}

Pos* createRandomPos() {
    Pos* p = (Pos*)malloc(sizeof(Pos));
    if (!p) {fprintf(stderr, "Memory allocation failed\n"); return NULL;}
    
    p->row = rand() % 50;
    p->col = rand() % 10;
    return p;
}

Book** createLibrary(int size) {
    Book** lib = (Book**)malloc(size * sizeof(Book*));
    if (!lib) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    for (int i = 0; i < size; ++i) {
        Pos* pos = createRandomPos();
        lib[i] = createBook(
            "Book",
            "Author",
            100 + i * 10,
            1990 + (i % 30),
            (GENRE)(i % 4),
            *pos
        );
        free(pos);
        if (!lib[i]) {
            for (int j = 0; j < i; ++j) free(lib[j]);
            free(lib);
            return NULL;
        }
    }
    return lib;
}

void printBook(const Book* b) {
    if (!b) {
        fprintf(stderr, "Invalid book\n");
        return;
    }
    const char* typeStr;
    switch (b->type) {
    case FICTION: typeStr = "Fiction";  break;
    case SCIENCE: typeStr = "Science";  break;
    case FANTASY: typeStr = "Fantasy";  break;
    case HISTORY: typeStr = "History";  break;
    default: typeStr = "Unknown";  break;
    }

    printf("Title: %s\n", b->title);
    printf("Author: %s\n", b->author);
    printf("Pages: %d\n", b->pages);
    printf("Year: %d\n", b->year);
    printf("Genre: %s\n", typeStr);
    printf("Position: (row %d, col %d)\n", b->position.row, b->position.col);
}


void serializeBook(const Book* b, const char* filename) {
    if (!b || !filename) {
        fprintf(stderr, "Invalid arguments\n");
        return;
    }
    FILE* file = fopen(filename, "wb");
    if (!file) {
        fprintf(stderr, "Failed to open file\n");
        return;
    }
    fwrite(b, sizeof(Book), 1, file);
    fclose(file);
}

Book* deserializeBook(const char* filename) {
    if (!filename) {
        fprintf(stderr, "Invalid filename\n");
        return NULL;
    }
    FILE* file = fopen(filename, "rb");
    if (!file) {
        fprintf(stderr, "Failed to open file\n");
        return NULL;
    }

    Book* b = (Book*)malloc(sizeof(Book));
    if (!b) {
        fprintf(stderr, "Memory allocation failed\n");
        fclose(file);
        return NULL;
    }

    fread(b, sizeof(Book), 1, file);
    fclose(file);
    return b;
}


int main(void) {
    srand((unsigned)time(NULL));

    Book* book = createBook("The C Programming Language", "Kernighan & Ritchie", 272, 1988, SCIENCE, (Pos){3, 14});
    if (!book) return -1;

    printBook(book);
    serializeBook(book, "book.dat");
    free(book);

    Book* loaded = deserializeBook("book.dat");
    if (loaded) {
        printBook(loaded);
        free(loaded);
    }

    int n = 5;
    Book** lib = createLibrary(n);
    if (lib) {
        for (int i = 0; i < n; ++i) {
            printf("#%d\n", i + 1);
            printBook(lib[i]);
            free(lib[i]);
        }
        free(lib);
    }
    return 0;
}
