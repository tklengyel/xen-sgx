# Copyright (C) 2004 Mike Wray <mike.wray@hp.com>

import os
from SrvDir import SrvDir
from xenmgr import sxp
from xenmgr import XendNode

class SrvNode(SrvDir):
    """Information about the node.
    """

    def __init__(self):
        SrvDir.__init__(self)
        self.xn = XendNode.instance()

    def op_shutdown(self, op, req):
        val = self.xn.shutdown()
        return val

    def op_reboot(self, op, req):
        val = self.xn.reboot()
        return val

    def op_cpu_rrobin_slice_set(self, op, req):
        fn = FormFn(self.xn.cpu_rrobin_slice_set,
                    [['slice', 'int']])
        val = fn(req.args, {})
        return val

    def op_cpu_bvt_slice_set(self, op, req):
        fn = FormFn(self.xn.cpu_bvt_slice_set,
                    [['slice', 'int']])
        val = fn(req.args, {})
        return val

    def render_POST(self, req):
        return self.perform(req)

    def render_GET(self, req):
        if self.use_sxp(req):
            req.setHeader("Content-Type", sxp.mime_type)
            sxp.show(['node'] + self.info(), out=req)
        else:
            req.write('<html><head></head><body>')
            self.print_path(req)
            req.write('<ul>')
            for d in self.info():
                req.write('<li> %10s: %s' % (d[0], d[1]))
            req.write('</ul>')
            req.write('</body></html>')
        return ''
            
    def info(self):
        (sys, host, rel, ver, mch) = os.uname()
        return [['system',  sys],
                ['host',    host],
                ['release', rel],
                ['version', ver],
                ['machine', mch]]
