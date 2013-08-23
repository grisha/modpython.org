#!/usr/bin/env python

import sys

print sys.argv[1]
s = open(sys.argv[1], 'w').read()


old = """
<script type="text/javascript"><!--
google_ad_client = "pub-9718360309690383";
google_ad_width = 120;
google_ad_height = 600;
google_ad_format = "120x600_as";
google_color_border = "CCCCCC";
google_color_bg = "FFFFFF";
google_color_link = "000000";
google_color_url = "666666";
google_color_text = "333333";
//--></script>
<script type="text/javascript"
  src="DISABLEhttp://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
"""
new = """
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-42971867-2', 'modpython.org');
  ga('send', 'pageview');
</script>

"""

s = s.replace(old, new)

print s

