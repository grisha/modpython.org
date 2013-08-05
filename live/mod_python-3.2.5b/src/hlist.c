/*
 * Copyright 2004 Apache Software Foundation 
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you
 * may not use this file except in compliance with the License.  You
 * may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.  See the License for the specific language governing
 * permissions and limitations under the License.
 *
 * Originally developed by Gregory Trubetskoy.
 *
 *
 * hlist.c 
 *
 * $Id: hlist.c 106619 2004-11-25 22:10:52Z nd $
 *
 * See accompanying documentation and source code comments 
 * for details.
 *
 */

#include "mod_python.h"

/**
 ** hlist_new
 **
 *  Start a new list.
 */

hl_entry *hlist_new(apr_pool_t *p, const char *h, const char *d, 
                    const int s)
{
    hl_entry *hle;

    hle = (hl_entry *)apr_pcalloc(p, sizeof(hl_entry));

    hle->handler = apr_pstrdup(p, h);
    hle->directory = apr_pstrdup(p, d);
    hle->silent = s;

    return hle;
}

/**
 ** hlist_append
 **
 *  Appends an hl_entry to a list identified by hle, 
 *  and returns the new tail. This func will skip
 *  to the tail of the list.
 *  If hle is NULL, a new list is created.
 */

hl_entry *hlist_append(apr_pool_t *p, hl_entry *hle, const char * h,
                       const char *d, const int s)
{
    hl_entry *nhle;

    /* find tail */
    while (hle && hle->next)
        hle = hle->next;

    nhle = (hl_entry *)apr_pcalloc(p, sizeof(hl_entry));

    nhle->handler = apr_pstrdup(p, h);
    nhle->directory = apr_pstrdup(p, d);
    nhle->silent = s;

    if (hle)
        hle->next = nhle;

    return nhle;
}

/**
 ** hlist_copy
 **
 */

hl_entry *hlist_copy(apr_pool_t *p, const hl_entry *hle)
{
    hl_entry *nhle;
    hl_entry *head;

    head = (hl_entry *)apr_pcalloc(p, sizeof(hl_entry));
    head->handler = apr_pstrdup(p, hle->handler);
    head->directory = apr_pstrdup(p, hle->directory);
    head->silent = hle->silent;

    hle = hle->next;
    nhle = head;
    while (hle) {
        nhle->next = (hl_entry *)apr_pcalloc(p, sizeof(hl_entry));
        nhle = nhle->next;
        nhle->handler = apr_pstrdup(p, hle->handler);
        nhle->directory = apr_pstrdup(p, hle->directory);
        nhle->silent = hle->silent;
        hle = hle->next;
    }

    return head;
}

