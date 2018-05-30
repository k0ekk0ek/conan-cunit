#include <stdio.h>
#include <stdlib.h>

#include "CUnit/CUnit.h"
#include "CUnit/Basic.h"

void
test_func(void)
{
    printf("%s\n", __func__);
    CU_ASSERT_EQUAL(2, 2);
    CU_ASSERT_NOT_EQUAL(0, -2);
    CU_ASSERT_FALSE(0);
    CU_ASSERT_TRUE(1);
}

static int
suite_init_func(void)
{
    printf("%s\n", __func__);
    return 0;
}

static int
suite_fini_func(void)
{
    printf("%s\n", __func__);
    return 0;
}

int
main(int argc, char *argv[])
{
    CU_ErrorCode code = CUE_SUCCESS;
    CU_pSuite suite = NULL;
    CU_pTest test = NULL;

    if ((code = CU_initialize_registry()) != CUE_SUCCESS) {
        fprintf(stderr, "CU_initialize_registry: %s\n", CU_get_error_msg());
    } else if ((suite = CU_add_suite("suite", &suite_init_func, &suite_fini_func)) == NULL) {
        code = CU_get_error();
        fprintf(stderr, "CU_add_suite: %s\n", CU_get_error_msg());
    } else if ((test = CU_add_test(suite, "test", &test_func)) == NULL) {
        code = CU_get_error();
        fprintf(stderr, "CU_add_test: %s\n", CU_get_error_msg());
    } else {
        CU_set_error_action(CUEA_IGNORE);
        CU_basic_set_mode(CU_BRM_NORMAL);
        CU_basic_run_tests();
    }

    return code == CUE_SUCCESS ? EXIT_SUCCESS : EXIT_FAILURE;
}

