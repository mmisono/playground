#define _GNU_SOURCE

#include <assert.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// All virtual pages are mapped into a single physical page
void *map(int num_pages)
{
    int fd, pagesize = getpagesize();
    void *area;
    char *start, *end, *p, *q;
    size_t length = pagesize * num_pages;

    // reserve virtual address space
    area = mmap(NULL, length, PROT_NONE,
                MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
    assert(area != MAP_FAILED);
    assert(munmap(area, length) == 0);

    // create temp file whose size is a pagesize
    fd = open("/tmp", O_TMPFILE | O_RDWR, 0600);
    assert(fd != -1);
    assert(ftruncate(fd, pagesize) == 0);

    // mmap each virtual page into the same physical page
    start = area;
    end = start + length;
    for (p = start; p < end; p += pagesize) {
        q = mmap(p, pagesize, PROT_READ | PROT_WRITE | PROT_EXEC,
                 MAP_SHARED | MAP_FIXED | MAP_POPULATE | MAP_NORESERVE, fd, 0);
        assert(p == q);
    }
    assert(close(fd) == 0);

    return area;
}

static uintptr_t virt_to_phys(void *virt)
{
    long pagesize = getpagesize();
    int fd = open("/proc/self/pagemap", O_RDONLY);
    assert(fd != -1);
    off_t ret =
        lseek(fd, (uintptr_t)virt / pagesize * sizeof(uintptr_t), SEEK_SET);
    assert(ret != -1);
    uintptr_t entry = 0;
    ssize_t rc = read(fd, &entry, sizeof(entry));
    assert(rc > 0);
    assert(entry != 0);
    assert(close(fd) == 0);

    return (entry & 0x7fffffffffffffULL) * pagesize +
           ((uintptr_t)virt) % pagesize;
}

int main()
{
    int pagesize = getpagesize();
    int i, num_pages = 100;
    char *p = map(num_pages);

    for (i = 0; i < num_pages; i++, p += pagesize) {
        printf("%016llx, %016llx\n", (unsigned long long)p,
               (unsigned long long)virt_to_phys(p));
    }

    return 0;
}
