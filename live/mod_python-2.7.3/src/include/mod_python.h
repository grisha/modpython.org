#ifndef Mp_MOD_PYTHON_H
#define Mp_MOD_PYTHON_H

/* ====================================================================
 * Copyright (c) 2000 Gregory Trubetskoy.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer. 
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * 3. The end-user documentation included with the redistribution, if
 *    any, must include the following acknowledgment: "This product 
 *    includes software developed by Gregory Trubetskoy."
 *    Alternately, this acknowledgment may appear in the software itself, 
 *    if and wherever such third-party acknowledgments normally appear.
 *
 * 4. The names "mod_python", "modpython" or "Gregory Trubetskoy" must not 
 *    be used to endorse or promote products derived from this software 
 *    without prior written permission. For written permission, please 
 *    contact grisha@ispol.com.
 *
 * 5. Products derived from this software may not be called "mod_python"
 *    or "modpython", nor may "mod_python" or "modpython" appear in their 
 *    names without prior written permission of Gregory Trubetskoy.
 *
 * THIS SOFTWARE IS PROVIDED BY GREGORY TRUBETSKOY ``AS IS'' AND ANY
 * EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL GREGORY TRUBETSKOY OR
 * HIS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 * ====================================================================
 *
 * mod_python.h 
 *
 * $Id: mod_python.h,v 1.13 2000/12/13 05:24:08 gtrubetskoy Exp $
 *
 * See accompanying documentation and source code comments 
 * for details.
 *
 * Apr 2000 - rename to mod_python and go apache-specific.
 * Nov 1998 - support for multiple interpreters introduced.
 * May 1998 - initial release (httpdapy).
 *
 */


/* Apache headers */
#include "httpd.h"
#include "http_config.h"
#include "http_core.h"
#include "http_main.h"
#include "http_protocol.h"
#include "util_script.h"
#include "http_log.h"


/* Python headers */
/* this gets rid of some comile warnings */
#if defined(_POSIX_THREADS)
#undef _POSIX_THREADS
#endif
#include "Python.h"
#include "structmember.h"

#if defined(WIN32) && !defined(WITH_THREAD)
#error Python threading must be enabled on Windows
#endif

#if !defined(WIN32)
#include <sys/socket.h>
#endif

/* _apache initialization function */
void init_apache();

/* pool given to us in ChildInit. We use it for 
   server.register_cleanup() */
extern pool *child_init_pool;

/* Apache module declaration */
extern module MODULE_VAR_EXPORT python_module;

#include "mpversion.h"
#include "util.h"
#include "tableobject.h"
#include "serverobject.h"
#include "connobject.h"
#include "requestobject.h"
/* #include "arrayobject.h" */

/** Things specific to mod_python, as an Apache module **/

#define VERSION_COMPONENT "mod_python/" MPV_STRING
#define MODULENAME "mod_python.apache"
#define INITFUNC "init"
#define MAIN_INTERPRETER "main_interpreter"
#ifdef WIN32
#define SLASH '\\'
#define SLASH_S "\\"
#else
#define SLASH '/'
#define SLASH_S "/"
#endif

PyObject *Mp_ServerReturn;

/* structure to hold interpreter data */
typedef struct {
    PyInterpreterState *istate;
    PyObject *obcallback;
} interpreterdata;

/* structure describing per directory configuration parameters */
typedef struct 
{
    int           authoritative;
    char         *config_dir;
    table        *options;
    table        *directives;
    table        *dirs;
} py_dir_config;

/* register_cleanup info */
typedef struct
{
    request_rec  *request_rec;
    server_rec   *server_rec;
    PyObject     *handler;
    const char   *interpreter;
    PyObject     *data;
} cleanup_info;

void python_cleanup(void *data);

#endif /* !Mp_MOD_PYTHON_H */
