#!/usr/local/bin/python3
import sys,json,os
import re
from lxml import etree


import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0,parentdir)

def log(*arg, **argv):
   # print(*arg,**argv)
    pass


class FilterHtml:
    tagBloacks = { "address", "article", "aside", "blockquote", "details", "dialog", "dd", "div", "dl", "dt",
        "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
        "header", "hgroup", "hr", "li", "main", "nav", "ol", "p", "pre", "section", "table", "ul",
        }
    tagIgnores = {'head', 'script'}
    TAG_START = 1
    TAG_ING = 2
    TAG_END = 3
    IGN_START = 4
    IGN_ING = 5
    IGN_END = 6
    NORMAL = 7
    def __init__(self,ss):
        self.origin_ = ss
        #(ob, oe,nb,ne) origin_begin/end, new_begin/end
        self.spanList_  = []
        self.plainTxt_  = ''
        self.build_()
        pass
    def __repr__(self):
        out  = ''
        for t in self.spanList_ :
            o = self.origin_[t[0]:t[1]]
            n = self.plainTxt_[t[2]: t[3]]
            out += f'[{n}]\t[{o}]\n----------------\n'
        #return self.plainTxt_
        return out

    @property
    def plainTxt(self):
        return self.plainTxt_


    def build_(self):
        #(ob, oe,nb,ne) origin_begin/end, new_begin/end
        ob, oe,nb,ne  = 0, -1,0,0
        #state
        tagState =  FilterHtml.TAG_END
        ignState =  FilterHtml.IGN_END
        ignTagName =  None

        tagStr  = ''
        nStr    = ''
        def addNew():
            nonlocal ob,oe,nb,ne
            nStrTrim = nStr.strip()
            if nStrTrim  == '':
                return
            ne += len(nStrTrim)
            self.spanList_.append((ob,oe, nb,ne) )
            self.plainTxt_  += nStrTrim
            ob  = oe
            nb  = ne
            pass

        for s in self.origin_:
            oe += 1
            if '<' == s:
                if '' != nStr:
                    addNew()
                nStr  = ''
                tagState = FilterHtml.TAG_START
                tagStr  = s
                continue
            elif '>' == s and tagState != FilterHtml.TAG_END:
                tagState = FilterHtml.TAG_END
                tagStr  += s
                r  = f'<\s*/\s*(\w+)[> ]'
                g =  re.match(r,tagStr, re.I)
                if g is not None:
                    curTag = g.group(1)
                    if curTag in FilterHtml.tagBloacks:
                        nStr += ".\n"
                    if ignState == FilterHtml.IGN_START and ignTagName is not None and ignTagName == curTag:
                        ignState =  FilterHtml.IGN_END
                        ignTagName = None
                        continue
                r  = f'<\s*(\w+)[> ]'
                g =  re.match(r,tagStr, re.I)
                if g is not None:
                    curTag = g.group(1)
                    if curTag in FilterHtml.tagIgnores:
                        ignState =  FilterHtml.IGN_START
                        ignTagName = g.group(1)
                        continue
                continue
            elif  tagState == FilterHtml.TAG_START or tagState == FilterHtml.TAG_ING:
                tagState = FilterHtml.TAG_ING
                tagStr  += s
                continue
            elif  FilterHtml.IGN_START == ignState:
                continue
            else:
                nStr  += s

        if '' != nStr:
            addNew()
        pass




def filterHtml_t():
    ss = """123 456<div> 789 <span> </div>
    <div>entern</div>
    dddddddd
    """
    h = FilterHtml(ss)
    print(h)
    ss = """0BBBBBBBB<head> hh<eee>hh </head>
    <a> aaaa </a>
    <b> bbbbbb </b>
    <b> take hhhhhhhhh <span> care <span> of </b>
    """
    h = FilterHtml(ss)
    print(h.plainTxt)


if __name__ == "__main__":
    filterHtml_t(); sys.exit(0)
    import doctest;doctest.testmod();sys.exit(0)
    testInput = ''
    newStr = ''.join([s for  o,n,s in filterHtml(testInput)])
    for  o,n,s in filterHtml(testInput):
        print(o,n,s)

testInput = """<!doctype>
<html lang="en-US" dir="ltr"> @@
  <head>
    <title>Security Agent causing high cpu - Apple Community</title>







    <link rel="next" href="https://discussions.apple.com/thread/250873047?page=2"/>



    <link rel="canonical" href="https://discussions.apple.com/thread/250873047"/>


		<link href="https://communities.apple.com/en202005220507/public/compiled/pages/thread.css" rel="stylesheet">
		<link rel="preload" href="https://communities.apple.com/en202005220507/public/compiled/pages/thread.js" as="script">



    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, minimum-scale=1, viewport-fit=cover">
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="encryption" data-status="enabled" data-x-token="disabled">

    <link rel="shortcut icon" href="https://communities.apple.com/en202005220507/public/assets/favicon.ico" type="image/x-icon">

    <meta name="ac-gn-store-key" content="S2A49YFKJF2JAT22K" />
<meta name="ac-gn-search-action" content="https://support.apple.com/kb/index" />
<meta name="ac-gn-search-input" content="q" />
<meta name="ac-gn-search-field[src]" content="globalnav_support" />
<meta name="ac-gn-search-field[type]" content="organic" />
<meta name="ac-gn-search-field[page]" content="search" />
<meta name="ac-gn-search-field[locale]" content="en_US" />
<link rel="stylesheet" type="text/css" href="//communities.apple.com/ac20190730/globalnav/4/en_US/styles/ac-globalnav.built.css">

    <link href="https://communities.apple.com/en202005220507/public/compiled/decorator.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="//communities.apple.com/ac20190730/globalfooter/3/en_US/styles/ac-globalfooter.built.css" />

    <link rel="preload" href="https://communities.apple.com/en202005220507/public/scripts/dtml.js" as="script">
    <link rel="preload" href="https://communities.apple.com/en202005220507/public/compiled/decorator.js" as="script">




<link rel="stylesheet" type="text/css" href="//communities.apple.com/wss20181115/fonts/?family=Apple+Icons&amp;v=1">


<link rel="stylesheet" type="text/css" href="//communities.apple.com/wss20181115/fonts?family&#x3D;Myriad+Set+Pro&amp;v&#x3D;1">
<link rel="stylesheet" type="text/css" href="//communities.apple.com/wss20181115/fonts?families&#x3D;SF+Pro,v1|SF+Pro+Icons,v1">

    <style type="text/css">
    div.post-body div.content-post-body-content * {
        position: relative !important;
        z-index:0!important;
    }
</style>
<script type="text/javascript">
    /** NONE **/
</script>
  </head>
  <body>

    <aside id="ac-gn-segmentbar" class="ac-gn-segmentbar" lang="en-US" dir="ltr" data-strings="{ 'exit': 'Exit', 'view': '{%STOREFRONT%} Store Home', 'segments': { 'smb': 'Business Store Home', 'eduInd': 'Education Store Home', 'other': 'Store Home' } }">
</aside>
<input type="checkbox" id="ac-gn-menustate" class="ac-gn-menustate" />
<nav id="ac-globalnav" class="no-js" role="navigation" aria-label="Global" data-hires="false" data-analytics-region="global nav" lang="en-US" dir="ltr" data-store-locale="us" data-store-api="//www.apple.com/[storefront]/shop/bag/status" data-search-locale="en_US" data-search-api="//www.apple.com/search-services/suggestions/">
	<div class="ac-gn-content">
		<ul class="ac-gn-header">
			<li class="ac-gn-item ac-gn-menuicon">
				<label class="ac-gn-menuicon-label" for="ac-gn-menustate" aria-hidden="true">
					<span class="ac-gn-menuicon-bread ac-gn-menuicon-bread-top">
						<span class="ac-gn-menuicon-bread-crust ac-gn-menuicon-bread-crust-top"></span>
					</span>
					<span class="ac-gn-menuicon-bread ac-gn-menuicon-bread-bottom">
						<span class="ac-gn-menuicon-bread-crust ac-gn-menuicon-bread-crust-bottom"></span>
					</span>
				</label>
				<a href="#ac-gn-menustate" role="button" class="ac-gn-menuanchor ac-gn-menuanchor-open" id="ac-gn-menuanchor-open">
					<span class="ac-gn-menuanchor-label">Global Nav Open Menu</span>
				</a>
				<a href="#" role="button" class="ac-gn-menuanchor ac-gn-menuanchor-close" id="ac-gn-menuanchor-close">
					<span class="ac-gn-menuanchor-label">Global Nav Close Menu</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-apple">
				<a class="ac-gn-link ac-gn-link-apple" href="//www.apple.com/" data-analytics-title="apple home" id="ac-gn-firstfocus-small">
					<span class="ac-gn-link-text">Apple</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-bag ac-gn-bag-small" id="ac-gn-bag-small">
				<a class="ac-gn-link ac-gn-link-bag" href="//www.apple.com/us/shop/goto/bag" data-analytics-title="bag" data-analytics-click="bag" aria-label="Shopping Bag" data-string-badge="Shopping Bag with item count :">
					<span class="ac-gn-link-text">Shopping Bag</span>
					<span class="ac-gn-bag-badge"></span>
				</a>
				<span class="ac-gn-bagview-caret ac-gn-bagview-caret-large"></span>
			</li>
		</ul>
		<div class="ac-gn-search-placeholder-container" role="search">
			<div class="ac-gn-search ac-gn-search-small">
				<a id="ac-gn-link-search-small" class="ac-gn-link" href="https://support.apple.com/kb/index?page=search&locale=en_US" data-analytics-title="search" data-analytics-click="search" data-analytics-intrapage-link aria-label="Search Support">
					<div class="ac-gn-search-placeholder-bar">
						<div class="ac-gn-search-placeholder-input">
							<div class="ac-gn-search-placeholder-input-text" aria-hidden="true">
								<div class="ac-gn-link-search ac-gn-search-placeholder-input-icon"></div>
								<span class="ac-gn-search-placeholder">Search Support</span>
							</div>
						</div>
						<div class="ac-gn-searchview-close ac-gn-searchview-close-small ac-gn-search-placeholder-searchview-close">
							<span class="ac-gn-searchview-close-cancel" aria-hidden="true">Cancel</span>
						</div>
					</div>
				</a>
			</div>
		</div>
		<ul class="ac-gn-list">
			<li class="ac-gn-item ac-gn-apple">
				<a class="ac-gn-link ac-gn-link-apple" href="//www.apple.com/" data-analytics-title="apple home" id="ac-gn-firstfocus">
						<span class="ac-gn-link-text">Apple</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-mac">
				<a class="ac-gn-link ac-gn-link-mac" href="//www.apple.com/mac/" data-analytics-title="mac">
						<span class="ac-gn-link-text">Mac</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-ipad">
				<a class="ac-gn-link ac-gn-link-ipad" href="//www.apple.com/ipad/" data-analytics-title="ipad">
						<span class="ac-gn-link-text">iPad</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-iphone">
				<a class="ac-gn-link ac-gn-link-iphone" href="//www.apple.com/iphone/" data-analytics-title="iphone">
						<span class="ac-gn-link-text">iPhone</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-watch">
				<a class="ac-gn-link ac-gn-link-watch" href="//www.apple.com/watch/" data-analytics-title="watch">
						<span class="ac-gn-link-text">Watch</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-tv">
				<a class="ac-gn-link ac-gn-link-tv" href="//www.apple.com/tv/" data-analytics-title="tv">
						<span class="ac-gn-link-text">TV</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-music">
				<a class="ac-gn-link ac-gn-link-music" href="//www.apple.com/music/" data-analytics-title="music">
						<span class="ac-gn-link-text">Music</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-support">
				<a class="ac-gn-link ac-gn-link-support current" href="https://support.apple.com" data-analytics-title="support">
						<span class="ac-gn-link-text">Support</span>
					</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-search" role="search">
				<a id="ac-gn-link-search" class="ac-gn-link ac-gn-link-search" href="https://support.apple.com/kb/index?page=search&locale=en_US" data-analytics-title="search" data-analytics-click="search" data-analytics-intrapage-link aria-label="Search Support"></a>
			</li>
			<li class="ac-gn-item ac-gn-bag" id="ac-gn-bag">
				<a class="ac-gn-link ac-gn-link-bag" href="//www.apple.com/us/shop/goto/bag" data-analytics-title="bag" data-analytics-click="bag" aria-label="Shopping Bag" data-string-badge="Shopping Bag with item count : {%BAGITEMCOUNT%}">
						<span class="ac-gn-link-text">Shopping Bag</span>
						<span class="ac-gn-bag-badge" aria-hidden="true"></span>
					</a>
				<span class="ac-gn-bagview-caret ac-gn-bagview-caret-large"></span>
			</li>
		</ul>
		<aside id="ac-gn-searchview" class="ac-gn-searchview" role="search" data-analytics-region="search">
			<div class="ac-gn-searchview-content">
				<div class="ac-gn-searchview-bar">
					<div class="ac-gn-searchview-bar-wrapper">
						<form id="ac-gn-searchform" class="ac-gn-searchform" action="//www.apple.com/us/search" method="get">
							<div class="ac-gn-searchform-wrapper">
								<input id="ac-gn-searchform-input" class="ac-gn-searchform-input" type="text" aria-label="Search Support" placeholder="Search Support" autocorrect="off" autocapitalize="off" autocomplete="off" spellcheck="false" role="combobox" aria-autocomplete="list" aria-expanded="true" aria-owns="quicklinks suggestions" />
								<input id="ac-gn-searchform-src" type="hidden" name="src" value="globalnav" />
								<button id="ac-gn-searchform-submit" class="ac-gn-searchform-submit" type="submit" disabled aria-label="Submit Search"></button>
								<button id="ac-gn-searchform-reset" class="ac-gn-searchform-reset" type="reset" disabled aria-label="Clear Search">
										<span class="ac-gn-searchform-reset-background"></span>
									</button>
							</div>
						</form>
						<button id="ac-gn-searchview-close-small" class="ac-gn-searchview-close ac-gn-searchview-close-small" aria-label="Cancel Search">
								<span class="ac-gn-searchview-close-cancel" aria-hidden="true">
									Cancel
								</span>
							</button>
					</div>
				</div>
				<aside id="ac-gn-searchresults" class="ac-gn-searchresults" data-string-quicklinks="Quick Links" data-string-suggestions="Suggested Searches" data-string-noresults=""></aside>
			</div>
			<button id="ac-gn-searchview-close" class="ac-gn-searchview-close" aria-label="Cancel Search">
					<span class="ac-gn-searchview-close-wrapper">
						<span class="ac-gn-searchview-close-left"></span>
						<span class="ac-gn-searchview-close-right"></span>
					</span>
				</button>
		</aside>
		<aside class="ac-gn-bagview" data-analytics-region="bag">
			<div class="ac-gn-bagview-scrim">
				<span class="ac-gn-bagview-caret ac-gn-bagview-caret-small"></span>
			</div>
			<div class="ac-gn-bagview-content" id="ac-gn-bagview-content">
			</div>
		</aside>
	</div>
</nav>
<div class="ac-gn-blur"></div>
<div id="ac-gn-curtain" class="ac-gn-curtain"></div>
<div id="ac-gn-placeholder" class="ac-nav-placeholder"></div>



    <div id="main-content">


<nav class="sub-nav-desktop" aria-label="Communities" data-analytics="nav:desktop">
  <div class="sub-nav-row top-row" role="presentation">
    <a href="/" class="subnav-title" data-analytics="nav:link">Communities</a>
    <a href="https://getsupport.apple.com" class="contact-support" data-analytics="nav:link">Contact Support</a>
  </div>
  <div class="sub-nav-row bottom-row" role="presentation">
    <div class="profile "  role="presentation">








<div class="dropdown" data-action="login-drop-down" data-auto-focus-first-item="true">

    <button class="drop-down-button text interactive" data-action="drop-down-button" >

      <span data-action="drop-down-button-text">Sign in</span>
    </button>
















<ul class="drop-down-menu plainText hidden"  data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/login" data-action="drop-down-menu-item">Sign in</a></li>

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/ilogin" data-action="drop-down-menu-item">Sign in corporate</a></li>

</ul>



</div>





    </div>
    <div class="nav" role="presentation">

      <a class="sub-nav-link" href="/browse" data-analytics="nav:link">Browse</a>
      <a class="sub-nav-link" href="/search" data-analytics="nav:link">Search</a>
















    </div>
  </div>
</nav>

<nav class="sub-nav-mobile" data-action="sub-nav-mobile-menu" aria-label="Communities" data-analytics="nav:mobile">
  <a href="/" class="subnav-title" data-analytics="nav:link">Communities</a>
  <input id="sub-nav-mobile-menu" type="checkbox" data-action="sub-nav-mobile-checkbox" class="a11y sub-nav-mobile-menu" aria-label="Open Communities Navigation Menu" role="button" aria-haspopup="true">
  <div class="sub-nav-wrapper" role="presentation">
      <div class="top">
        <label for="sub-nav-mobile-menu" class="chevron-icon" data-action="sub-nav-mobile-menu-label">
          <div class="line left"></div>
          <div class="line right"></div>
        </label>
      </div>
      <ul class="nav" role="presentation" data-action="sub-nav-mobile-menu-list">



            <li role="presentation"><button class="menu-item mobile-login-link" data-action="mobile-login-link" tabindex="0">Sign in</button></li>





            <li role="presentation"><a class="menu-item" href="/create/question?communityId=250000076020" data-action="to-mobile-post-creation" data-analytics="nav:link">Post</a></li>



        <li role="presentation"><a class="menu-item" href="/browse"  data-analytics="nav:link">Browse</a></li>





        <li role="presentation"><a class="menu-item" href="https://getsupport.apple.com" data-analytics="nav:link">Contact Support</a></li>



        <li class="sub-menu-search" role="presentation">
          <form action="/create/question?communityId=250000076020" class="search-form-menu" method="GET" data-action="menu-search-form">
            <div class="cover" data-action="menu-search-cover" tabindex="0" role="button" data-analytics="nav:search"><span class="a11y">Ask a question</span></div>
            <input type="text" aria-required="true" aria-label="Ask a question" id="askaquestion-menu" name="subject" required autocomplete="off" maxlength="250" placeholder="Search or ask a question" aria-invalid="false" data-action="menu-search">
          </form>
        </li>
        <label class="a11y" aria-label="Close Communities Navigation Menu" role="button" for="sub-nav-mobile-menu"></label>
      </ul>
      <div class="dim" data-action="sub-nav-mobile-dim"></div>
  </div>
</nav>





	<nav class="breadcrumbs" aria-label="Communities Breadcrumbs" data-analytics="nav:breadcrumb">
		<a href="/" data-analytics="nav:link">Support Communities</a>

			<span class="pipe" aria-hidden="true">/</span>
			<a href="/community/mac_os"  data-analytics="nav:link">
				Mac OS &amp; System Software
			</a>

			<span class="pipe" aria-hidden="true">/</span>
			<a href="/community/mac_os/catalina" class="show-bold" data-analytics="nav:link">
				macOS Catalina
			</a>

	</nav>



    <main class="page" role="main" data-thread-id="250873047" data-analytics="thread:page" data-analytics-community="catalina" data-analytics-subcommunity="mac_os" data-analytics-thread-id="250873047" data-analytics-replies-count="45" itemscope="itemscope" itemtype="http://schema.org/QAPage">

      <link itemprop="url" href="https://discussions.apple.com/thread/250873047">





      <div itemscope="itemscope" itemprop="mainEntity" itemtype="http://schema.org/Question">




        <div data-action="thread-question">


<section role="region"

    aria-label="Thread question" aria-describedby="content-post-title"
    id="250873047021"





  class="content-post question" data-analytics="thread-question" data-analytics-id="250873047" data-action="thread-question">


    <meta itemprop="answerCount" content="45" />


  <div class="header" data-action="content-post-header">









      <div class="post-author-profile author-content large">



  <a
    class="user-avatar"


        href="/profile/admiral+u"

      data-action="common-user-avatar"
      data-user-id="5b8aad917c4b38ea"


  >

  <span class="a11y">
    User profile for user:

      admiral u

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_1153.png"
  class="avatar-contain large-avatar"
  alt="admiral u"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" itemscope="itemscope" itemprop="author" itemtype="http://schema.org/Person">
          <a
            class="post-author-name"


                href="/profile/admiral+u"

              data-action="content-post-user"
              data-user-id="5b8aad917c4b38ea"

          >
            <span class="author-name" itemprop="name">
              admiral u
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (20 points)
                </span>




                <span class="expertise">



<div class="user-expertise question">
  <span><div class="user-expertise-icon experertise-macosx" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">macOS<span class="a11y">Speciality level out of ten: 0</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-0"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">

      <span class="drop-cap hide-tablet">
        <span class="a11y">Question:</span>
        <span aria-hidden="true">Q:</span>
      </span>



    <div class="post-content">

        <h1 class="title question-title" id="content-post-title" data-action="content-post-title">

            <span class="a11y show-tablet-inline">Question:</span>
            <span class="drop-cap show-tablet-inline" aria-hidden="true">Q:</span>


            <span itemprop="name" data-action="content-post-title-text">Security Agent causing high cpu</span>

        </h1>








      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" itemprop="text"><p>I&#39;ve noticed in Activity Monitor that the &#34;Security Agent&#34; process is consuming 100% of a CPU core. What&#39;s more is that there are 4 &#34;Security Agent&#34; processes running, each at 100%! </p><p><br /></p><p>I&#39;ve noticed this problem happens every 7 days or so and I can&#39;t figure out why. The only reason I notice is that I come up to my iMac and the fans are running trying to cool the thing as it struggles with the runs away &#34;Security Agent&#34; processes.</p><p><br /></p><p>Please help!</p><p><br /></p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>



          <p class="signature hide-tablet">

              iMac 27&quot;,


              10.15


          </p>




        <p class="timestamp">



                Posted on <time itemprop="dateCreated" datetime="2019-11-19T18:22Z">Nov 19, 2019 6:22 PM</time>




        </p>


      <div class="action-bar" data-action="content-post-action-bar">


            <a class="button button-black" href="/login?replyId=250873047021" data-analytics="content-post:action:reply:link">Reply</a>



            <button class="button me-too button-white" data-action="content-post-me-too" data-analytics="content-post:action:metoo" data-post-id="250873047021">
              <span class="button-large button-default">
                I have this question too&nbsp;(<span itemprop="upvoteCount">216</span>)
              </span>
              <span class="button-large button-clicked">
                <span class="icon icon-check"></span>
                <span>I have this question too</span>
              </span>
              <span class="button-small button-default">
                Me too&nbsp;(216)
              </span>
              <span class="button-small button-clicked">
                <span class="icon icon-check"></span>
                <span>Me too</span>
              </span>
            </button>

          <div class="no-display show-tablet-inline-block">











          </div>







      </div>
    </div>
  </div>
</section>





<section role="region"


    aria-label="Best answer"
    data-analytics-solved="false"
    data-analytics-helpful="true"
    data-analytics-recommended="true"

      itemscope="itemscope"
      itemprop="acceptedAnswer"
      itemtype="http://schema.org/Answer"





  class="content-post top-answer" data-analytics="top-answer" data-analytics-id="251656910" >



  <div class="header" data-action="content-post-header">




              <span class="post-status post-recommended" data-action="post-status">
                <span class="a11y">Question marked as</span>
                <span class="icon icon-apple recommended-post" aria-hidden="true"></span>
                Apple recommended
              </span>












      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/Kappy"

      data-action="common-user-avatar"
      data-user-id="5622b257a40d781f"


  >

  <span class="a11y">
    User profile for user:

      Kappy

  </span>
  <img src="/assets/avatar/5622b257a40d781f/848f5d260fe1fb746a69fb4ae000cecf4cd80f862181dbc545d5c1adf4077a55"
  class="avatar-contain default-avatar"
  alt="Kappy"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" itemscope="itemscope" itemprop="author" itemtype="http://schema.org/Person">
          <a
            class="post-author-name"


                href="/profile/Kappy"

              data-action="content-post-user"
              data-user-id="5622b257a40d781f"

          >
            <span class="author-name" itemprop="name">
              Kappy
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-10" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;10

    </span>
  </div>




                <span class="points">
                  (350,226 points)
                </span>




                <span class="expertise">



<div class="user-expertise top-answer">
  <span><div class="user-expertise-icon experertise-desktops" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">Desktops<span class="a11y">Speciality level out of ten: 1</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-1"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">


      <span class="drop-cap hide-tablet">
        <span class="a11y">Answer:</span>
        <span aria-hidden="true">A:</span>
      </span>


    <div class="post-content">








      <div class="post-body" data-action="content-post-body">

          <span class="a11y show-tablet-inline">Answer:</span>
          <span class="drop-cap show-tablet-inline" aria-hidden="true">A:</span>


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" itemprop="text"><p>I do not see such a process on my system. I found a reference in one of the Developers manuals:</p><p><br /></p><p class="indent-1"><strong>Security Agent</strong></p><p class="indent-1">The <em>Security Agent</em> is a separate process that provides the user interface for the Security Server in macOS (not iOS). Its primary purpose is to request authentication whenever an app requests additional privileges.</p><p class="indent-1">When the Security Server requires the user to authenticate, the Security Agent displays a dialog requesting a user name and password. The advantages of performing this action in a separate process are twofold. First, an application can obtain authorization without ever having access to the user’s credentials (username and password, for example). Second, it enables Apple to add new forms of authentication without requiring every application to understand them.</p><p class="indent-1">The Security Agent requires that the user be physically present in order to be authenticated. Because the graphical user interface elements can’t be used through a command-line interface such as the Terminal app or a secure shell (ssh) remote session, this restriction makes it much more difficult for a malicious user to breach an app’s security.</p><p><br /></p><p>Perhaps this may help you track down what is causing the problem. One thing you might try:</p><p><br /></p><p><strong>About Safe Mode</strong></p><p><br /></p><ul><li><a href="https://support.apple.com/en-us/HT201262" target="_blank" rel="nofollow noopener noreferrer"><u>Use safe mode to isolate issues with your Mac - Apple Support</u></a></li><li><a href="https://eclecticlight.co/2016/08/24/playing-safe-what-does-safe-mode-do/" target="_blank" rel="nofollow noopener noreferrer"><u>Playing Safe- what does Safe mode do?</u></a></li></ul><p><br /></p><p>Boot into safe mode then restart normally. This clears out a number of caches which may stop the process from eating up so much CPU time. Safe mode is much slower than a normal startup, so be patient.</p><p><br /></p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp">




                Posted on <time itemprop="dateCreated" datetime="2019-11-19T19:57Z">Nov 19, 2019 7:57 PM</time>



        </p>


      <div class="action-bar" data-action="content-post-action-bar">



          <a class="button button-white" href="https://discussions.apple.com/thread/250873047?answerId&#x3D;251656910022#251656910022" data-analytics="content-post:action:view-in-context" itemprop="url">View answer in context</a>





      </div>
    </div>
  </div>
</section>


        </div>



            <div class="helpful-all-toggler" data-action="helpful-all-toggler">







<div class="dropdown">









    <div class="drop-down-header-wrapper" data-action="drop-down-button">
      <h2 data-action="drop-down-button-text" class="drop-down-header ">
        All replies
      </h2>
      <button class="drop-down-button header"  disabled aria-haspopup="true" aria-expanded="false"  >
        <span></span>
        <span class="a11y">Drop Down menu</span>
      </button>
    </div>







</div>




            </div>



        <section class="all-replies"  data-action="all-replies" role="region" aria-label="All replies">


              <div class="top-pagination hide-tablet">



<nav class="pagination" data-action="pagination" role="navigation" aria-label="Pagination" data-current-page="1" data-total-pages="3">
  <ol class="pagination-list" role="presentation">
    <li>
      <a class="first-page hidden" href="/thread/250873047" aria-label="First page" data-action="pagination-first" role="button">
        first
      </a>
    </li>

    <li>
      <a class="previous-page icon icon-standalone icon-chevronleft hidden" role="button" href="#" aria-label="Previous page" data-action="pagination-prev">
      </a>
    </li>

    <li>
      <span class="page-number" role="text" aria-label="Page 1 of 3">

          <span class="hide-mobile-inline-block" data-action="pagination-page-number-text">
            Page 1 of 3
          </span>
          <span class="hide-desktop-inline-block" data-action="pagination-page-number-text-mobile">
            Page 1/3
          </span>

      </span>
    </li>

    <li>
      <a class="next-page icon icon-standalone icon-chevronright" role="button" data-action="pagination-next" href="?page=2" aria-label="Next page">
      </a>
    </li>


      <li>
        <a class="last-page" href="?page=3" aria-label="Last page" role="button" data-action="pagination-last">
          last
        </a>
      </li>

  </ol>
</nav>



    <div class="pagination-overlay" aria-hidden="true" data-analytics="pagination-overlay">
      <span data-action="pagination-page-number-text-mobile">
        Page 1/3
      </span>
    </div>



              </div>


          <div data-action="all-replies-content" class="all-replies-content">



<div class="spinner-wrapper hidden" data-action="loading-ajax-data">



<p class="a11y"  aria-hidden="false"   tabindex="-1" data-action="aria-label">Loading page content</p>


  <div class="spinner"></div>
</div>




<p class="a11y"  aria-hidden="true"   tabindex="-1" data-action="ajax-data-aria-live">Page content loaded</p>








<article





    id="251656910022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251656910" data-action="thread-reply">



  <div class="header" data-action="content-post-header">




              <span class="post-status post-recommended" data-action="post-status">
                <span class="a11y">Question marked as</span>
                <span class="icon icon-apple recommended-post" aria-hidden="true"></span>
                Apple recommended
              </span>












      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/Kappy"

      data-action="common-user-avatar"
      data-user-id="5622b257a40d781f"


  >

  <span class="a11y">
    User profile for user:

      Kappy

  </span>
  <img src="/assets/avatar/5622b257a40d781f/848f5d260fe1fb746a69fb4ae000cecf4cd80f862181dbc545d5c1adf4077a55"
  class="avatar-contain default-avatar"
  alt="Kappy"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/Kappy"

              data-action="content-post-user"
              data-user-id="5622b257a40d781f"

          >
            <span class="author-name" >
              Kappy
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-10" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;10

    </span>
  </div>




                <span class="points">
                  (350,226 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-desktops" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">Desktops<span class="a11y">Speciality level out of ten: 1</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-1"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;250873047021#250873047021">
              <span class="hide-tablet-inline">

                  Nov 19, 2019 7:57 PM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>I do not see such a process on my system. I found a reference in one of the Developers manuals:</p><p><br /></p><p class="indent-1"><strong>Security Agent</strong></p><p class="indent-1">The <em>Security Agent</em> is a separate process that provides the user interface for the Security Server in macOS (not iOS). Its primary purpose is to request authentication whenever an app requests additional privileges.</p><p class="indent-1">When the Security Server requires the user to authenticate, the Security Agent displays a dialog requesting a user name and password. The advantages of performing this action in a separate process are twofold. First, an application can obtain authorization without ever having access to the user’s credentials (username and password, for example). Second, it enables Apple to add new forms of authentication without requiring every application to understand them.</p><p class="indent-1">The Security Agent requires that the user be physically present in order to be authenticated. Because the graphical user interface elements can’t be used through a command-line interface such as the Terminal app or a secure shell (ssh) remote session, this restriction makes it much more difficult for a malicious user to breach an app’s security.</p><p><br /></p><p>Perhaps this may help you track down what is causing the problem. One thing you might try:</p><p><br /></p><p><strong>About Safe Mode</strong></p><p><br /></p><ul><li><a href="https://support.apple.com/en-us/HT201262" target="_blank" rel="nofollow noopener noreferrer"><u>Use safe mode to isolate issues with your Mac - Apple Support</u></a></li><li><a href="https://eclecticlight.co/2016/08/24/playing-safe-what-does-safe-mode-do/" target="_blank" rel="nofollow noopener noreferrer"><u>Playing Safe- what does Safe mode do?</u></a></li></ul><p><br /></p><p>Boot into safe mode then restart normally. This clears out a number of caches which may stop the process from eating up so much CPU time. Safe mode is much slower than a normal startup, so be patient.</p><p><br /></p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Nov 19, 2019 7:57 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251656910022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251656910022">Helpful&nbsp;(4)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251656910022#251656910022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251658624022"
    tabindex="-1"

  class="content-post answer own-answer" data-analytics="thread-answer" data-analytics-id="251658624" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/admiral+u"

      data-action="common-user-avatar"
      data-user-id="5b8aad917c4b38ea"


  >

  <span class="a11y">
    User profile for user:

      admiral u

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_1153.png"
  class="avatar-contain default-avatar"
  alt="admiral u"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/admiral+u"

              data-action="content-post-user"
              data-user-id="5b8aad917c4b38ea"

          >
            <span class="author-name" >
              admiral u
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (20 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-macosx" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">macOS<span class="a11y">Speciality level out of ten: 0</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-0"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251656910022#251656910022">
              <span class="hide-tablet-inline">

                  Nov 20, 2019 5:33 AM in response to Kappy

              </span>
              <span class="show-tablet-inline">

                  In response to Kappy

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>Thanks Kappy, this is helpful. The problem goes away when I reboot the machine (safe mode or not). Once I start back up I don&#39;t see the process either. Maybe while I am away the Security Agent is trying to display a dialog or ask my permission to do something and can&#39;t? I&#39;ll try booting into safe mode and see if clearing those caches you mentioned helps.</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Nov 20, 2019 5:33 AM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251658624022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251658624022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251658624022#251658624022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251738481022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251738481" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/mshearer6"

      data-action="common-user-avatar"
      data-user-id="f7ed90dfdab896c"


  >

  <span class="a11y">
    User profile for user:

      mshearer6

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_8999.png"
  class="avatar-contain default-avatar"
  alt="mshearer6"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/mshearer6"

              data-action="content-post-user"
              data-user-id="f7ed90dfdab896c"

          >
            <span class="author-name" >
              mshearer6
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-macosx" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">macOS<span class="a11y">Speciality level out of ten: 0</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-0"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;250873047021#250873047021">
              <span class="hide-tablet-inline">

                  Dec 4, 2019 6:17 PM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>I force stop the process in Activity monitor, but I am annoyed as it keeps coming back.  I also have not been able to sort out what is causing it.  Never happened before I upgraded to Catalina.  Most annoying issue.</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Dec 4, 2019 6:17 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251738481022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251738481022">Helpful&nbsp;(1)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251738481022#251738481022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251771282022"
    tabindex="-1"

  class="content-post answer own-answer" data-analytics="thread-answer" data-analytics-id="251771282" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/admiral+u"

      data-action="common-user-avatar"
      data-user-id="5b8aad917c4b38ea"


  >

  <span class="a11y">
    User profile for user:

      admiral u

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_1153.png"
  class="avatar-contain default-avatar"
  alt="admiral u"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/admiral+u"

              data-action="content-post-user"
              data-user-id="5b8aad917c4b38ea"

          >
            <span class="author-name" >
              admiral u
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (20 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-macosx" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">macOS<span class="a11y">Speciality level out of ten: 0</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-0"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251738481022#251738481022">
              <span class="hide-tablet-inline">

                  Dec 10, 2019 7:29 PM in response to mshearer6

              </span>
              <span class="show-tablet-inline">

                  In response to mshearer6

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>Some additional Information. I&#39;ve noticed these messages in the Console, under Log Reports, wifi.log. This repeats over and over again.</p><p><br /></p><pre class="ql-syntax" spellcheck="false"><code aria-label="Code">Tue Dec 10 11:02:50.848 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events.private, will not register for event type 100
Tue Dec 10 11:02:50.848 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events.private, will not register for event type 101
Tue Dec 10 11:02:50.848 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events, but allowing anyways for event type 7
Tue Dec 10 11:02:50.848 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events, but allowing anyways for event type 2
Tue Dec 10 11:02:50.848 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events, but allowing anyways for event type 1
Tue Dec 10 11:02:50.848 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events, but allowing anyways for event type 5
Tue Dec 10 11:02:50.849 &lt;airportd[246]&gt; ERROR: SecurityAgent (5615) is not entitled for com.apple.wifi.events, but allowing anyways for event type 6
</code></pre></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Dec 10, 2019 7:29 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251771282022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251771282022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251771282022#251771282022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251771506022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251771506" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/Kappy"

      data-action="common-user-avatar"
      data-user-id="5622b257a40d781f"


  >

  <span class="a11y">
    User profile for user:

      Kappy

  </span>
  <img src="/assets/avatar/5622b257a40d781f/848f5d260fe1fb746a69fb4ae000cecf4cd80f862181dbc545d5c1adf4077a55"
  class="avatar-contain default-avatar"
  alt="Kappy"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/Kappy"

              data-action="content-post-user"
              data-user-id="5622b257a40d781f"

          >
            <span class="author-name" >
              Kappy
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-10" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;10

    </span>
  </div>




                <span class="points">
                  (350,226 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-desktops" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">Desktops<span class="a11y">Speciality level out of ten: 1</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-1"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251771282022#251771282022">
              <span class="hide-tablet-inline">

                  Dec 10, 2019 8:41 PM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>Related to Airport network. &#34;airportd&#34; is a daemon/driver. Call Apple to find out more.</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Dec 10, 2019 8:41 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251771506022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251771506022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251771506022#251771506022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251850690022"
    tabindex="-1"

  class="content-post answer own-answer" data-analytics="thread-answer" data-analytics-id="251850690" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/admiral+u"

      data-action="common-user-avatar"
      data-user-id="5b8aad917c4b38ea"


  >

  <span class="a11y">
    User profile for user:

      admiral u

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_1153.png"
  class="avatar-contain default-avatar"
  alt="admiral u"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/admiral+u"

              data-action="content-post-user"
              data-user-id="5b8aad917c4b38ea"

          >
            <span class="author-name" >
              admiral u
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (20 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-macosx" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">macOS<span class="a11y">Speciality level out of ten: 0</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-0"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;250873047021#250873047021">
              <span class="hide-tablet-inline">

                  Dec 25, 2019 11:48 AM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>Just an update, I have not seen this issue since the macOS 10.15.2 patch was installed on my iMac. I also turned off my wifi (I have an ethernet connection) so it seems that one of those fixed things. </p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Dec 25, 2019 11:48 AM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251850690022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251850690022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251850690022#251850690022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251851235022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251851235" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/TheLittles"

      data-action="common-user-avatar"
      data-user-id="d87328de22a9f5d60481d7d804c08cac"


  >

  <span class="a11y">
    User profile for user:

      TheLittles

  </span>
  <img src="/assets/avatar/d87328de22a9f5d60481d7d804c08cac/6ed4986bf0f270088055d64832b4c0c9e5197f8326bfc0ea852a7109981ab105"
  class="avatar-contain default-avatar"
  alt="TheLittles"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/TheLittles"

              data-action="content-post-user"
              data-user-id="d87328de22a9f5d60481d7d804c08cac"

          >
            <span class="author-name" >
              TheLittles
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-6" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;6

    </span>
  </div>




                <span class="points">
                  (13,289 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-iphone" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">iPhone<span class="a11y">Speciality level out of ten: 10</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-10"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251850690022#251850690022">
              <span class="hide-tablet-inline">

                  Dec 25, 2019 1:47 PM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p><strong>admiral u Said:</strong></p><p>&#34;<em>Just an update, I have not seen this issue since the macOS 10.15.2 patch was installed on my iMac. I also turned off my wifi (I have an ethernet connection) so it seems that one of those fixed things.</em>&#34;</p><p>-------</p><p><br /></p><p><strong>Inform Apple of the Update&#39;s Fix:</strong></p><p>Inform <em>Apple</em> of this.  Provide them feedback on this.  I think it is extremely important that their engineers know about positive impacts any update whatsoever may have had on issues that may or may not have been intentionally fixed by the installation of the update.  So,...</p><ol><li><strong>Go Here: </strong><a href="https://www.google.com/url?sa&#61;t&amp;rct&#61;j&amp;q&#61;&amp;esrc&#61;s&amp;source&#61;web&amp;cd&#61;1&amp;ved&#61;2ahUKEwiFqdaL4dHmAhXy1FkKHYV6CxgQFjAAegQIBBAB&amp;url&#61;https%3A%2F%2Fwww.apple.com%2Ffeedback%2Fmacos.html&amp;usg&#61;AOvVaw31DcKISjnl9CWRLZqorEYZ" target="_blank" rel="nofollow noopener noreferrer">Feedback - macOS - Apple</a></li><li><strong>Select:</strong> &#34;<em>Performance</em>&#34; for the &#34;<em>Feedback Type</em>&#34;</li><li><strong>Select:</strong> &#34;<em>Software/Firmware Update</em>&#34; for the &#34;<em>Feedback Area</em>&#34;</li><li><strong>Proceed from there as Necessary</strong></li></ol></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Dec 25, 2019 1:47 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251851235022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251851235022">Helpful&nbsp;(1)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251851235022#251851235022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251909904022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251909904" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/bvramana"

      data-action="common-user-avatar"
      data-user-id="7ab5cac3ad277a60"


  >

  <span class="a11y">
    User profile for user:

      bvramana

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_8999.png"
  class="avatar-contain default-avatar"
  alt="bvramana"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/bvramana"

              data-action="content-post-user"
              data-user-id="7ab5cac3ad277a60"

          >
            <span class="author-name" >
              bvramana
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251771282022#251771282022">
              <span class="hide-tablet-inline">

                  Jan 4, 2020 6:24 PM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>Today i observed same behaviour on my MBP 16&#34;.  Same logs - restart of machine did stop it. I am on 10.15.2 as well. </p><p><br /></p><p>not sure whats behind this behaviour. Cant move to LAN as mostly i am on Wifi</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Jan 4, 2020 6:24 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251909904022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251909904022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251909904022#251909904022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251916882022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251916882" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/yx66"

      data-action="common-user-avatar"
      data-user-id="c73d27082b7afe2b5b548d82e9abab7e"


  >

  <span class="a11y">
    User profile for user:

      yx66

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR.png"
  class="avatar-contain default-avatar"
  alt="yx66"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/yx66"

              data-action="content-post-user"
              data-user-id="c73d27082b7afe2b5b548d82e9abab7e"

          >
            <span class="author-name" >
              yx66
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251909904022#251909904022">
              <span class="hide-tablet-inline">

                  Jan 6, 2020 1:00 AM in response to bvramana

              </span>
              <span class="show-tablet-inline">

                  In response to bvramana

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>I have this problem as well the security process took 100% of CPU with the Catalina..........and I still haven’t got the reason why</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Jan 6, 2020 1:00 AM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251916882022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251916882022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251916882022#251916882022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251922120022"
    tabindex="-1"

  class="content-post answer own-answer" data-analytics="thread-answer" data-analytics-id="251922120" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/admiral+u"

      data-action="common-user-avatar"
      data-user-id="5b8aad917c4b38ea"


  >

  <span class="a11y">
    User profile for user:

      admiral u

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_1153.png"
  class="avatar-contain default-avatar"
  alt="admiral u"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/admiral+u"

              data-action="content-post-user"
              data-user-id="5b8aad917c4b38ea"

          >
            <span class="author-name" >
              admiral u
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (20 points)
                </span>




                <span class="expertise">



<div class="user-expertise answer">
  <span><div class="user-expertise-icon experertise-macosx" aria-hidden="true"></div></span>
  <div class="expertise-info">
    <div class="expertise-title">macOS<span class="a11y">Speciality level out of ten: 0</span></div>
    <span class="progress-bar">
      <span class="dashes progress-level-0"></span>
      <span class="progress-dashes"></span>
    </span>
  </div>
</div>



                </span>


          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;250873047021#250873047021">
              <span class="hide-tablet-inline">

                  Jan 6, 2020 5:45 PM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>The issue is back. I am now thinking it is related to my daughter logging into the iMac with her account which is under parental control. Really disappointing. </p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Jan 6, 2020 5:45 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251922120022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251922120022">Helpful&nbsp;(3)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251922120022#251922120022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251923612022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251923612" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/yx66"

      data-action="common-user-avatar"
      data-user-id="c73d27082b7afe2b5b548d82e9abab7e"


  >

  <span class="a11y">
    User profile for user:

      yx66

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR.png"
  class="avatar-contain default-avatar"
  alt="yx66"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/yx66"

              data-action="content-post-user"
              data-user-id="c73d27082b7afe2b5b548d82e9abab7e"

          >
            <span class="author-name" >
              yx66
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251922120022#251922120022">
              <span class="hide-tablet-inline">

                  Jan 7, 2020 2:27 AM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>you should install windows&#xff0c; Macos is not mature</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Jan 7, 2020 2:27 AM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251923612022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251923612022">Helpful&nbsp;(3)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251923612022#251923612022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="251923702022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="251923702" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/bvramana"

      data-action="common-user-avatar"
      data-user-id="7ab5cac3ad277a60"


  >

  <span class="a11y">
    User profile for user:

      bvramana

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_8999.png"
  class="avatar-contain default-avatar"
  alt="bvramana"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/bvramana"

              data-action="content-post-user"
              data-user-id="7ab5cac3ad277a60"

          >
            <span class="author-name" >
              bvramana
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251916882022#251916882022">
              <span class="hide-tablet-inline">

                  Jan 7, 2020 2:50 AM in response to yx66

              </span>
              <span class="show-tablet-inline">

                  In response to yx66

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>i see this issue occurring for me as well as for others when twp or more users are logged in (you can check with tick marks on the lock screen if it is 1 or 2 or more depending on number of users one has created on the mac). </p><p><br /></p><p>it just keeps these fans ON most of the time as this process uses 100% CPU.. 8 core i9 or 32GB RAM is of no use or help :-)</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Jan 7, 2020 2:50 AM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=251923702022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=251923702022">Helpful&nbsp;(1)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;251923702022#251923702022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="252070254022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="252070254" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/Stickman32"

      data-action="common-user-avatar"
      data-user-id="df920ade00ace16"


  >

  <span class="a11y">
    User profile for user:

      Stickman32

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_8999.png"
  class="avatar-contain default-avatar"
  alt="Stickman32"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/Stickman32"

              data-action="content-post-user"
              data-user-id="df920ade00ace16"

          >
            <span class="author-name" >
              Stickman32
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;250873047021#250873047021">
              <span class="hide-tablet-inline">

                  Feb 1, 2020 10:03 AM in response to admiral u

              </span>
              <span class="show-tablet-inline">

                  In response to admiral u

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>I have (had) the same issue with a new 16&#34; MacBook Pro (spec, activity monitor &amp; Intel Powergadget monitoring attached)</p><p><br /></p><p>&#34;SecurityAgent&#34; pushes the CPU up to about 4.3Ghz then sits back watching the temperature rise and the battery drain... for no apparent reason. I left it for about 30 mins to see where it would go. It gets the CPU up to about 80C then leaves it simmering, until you decide to re-boot the computer. </p><p><br /></p><p>I&#39;ve also had issues with it forgetting an external monitor is attached via CalDigit TS3&#43; when it sleeps, which requires a re-boot.... and of course with a monitor attached the extra strain on the GPU stresses the cooling so the CPU is often sitting at 100C which I can&#39;t imagine is good for it long term.</p><p><br /></p><p>I intimated past tense in my first paragraph with the word &#34;had&#34;... because I returned the machine to Apple this afternoon for a refund. I was hoping it would be a worthy replacement for my 8 year old Mac Pro.... but alas, I think they are still trying to squeeze too much grunt into too small a space. </p><p><br /></p><p>Form above function... no, not when I rely on this for my living.</p><p><br /></p><p>SM</p><p><br /></p><p><br /></p><p><br /></p><p><img src="https://discussions.apple.com/content/attachment/322cd958-237e-44ed-82ab-a4d5e43297cd" aria-label="User uploaded image 1" /><img src="https://discussions.apple.com/content/attachment/3839e4f5-13aa-4705-a6ba-3952970a7193" aria-label="User uploaded image 2" /></p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Feb 1, 2020 10:03 AM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=252070254022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=252070254022">Helpful&nbsp;(1)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;252070254022#252070254022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="252071336022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="252071336" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/_MiB_"

      data-action="common-user-avatar"
      data-user-id="bb29c757707a22ef9d09c0ff37be2bc3"


  >

  <span class="a11y">
    User profile for user:

      _MiB_

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR.png"
  class="avatar-contain default-avatar"
  alt="_MiB_"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/_MiB_"

              data-action="content-post-user"
              data-user-id="bb29c757707a22ef9d09c0ff37be2bc3"

          >
            <span class="author-name" >
              _MiB_
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;252070254022#252070254022">
              <span class="hide-tablet-inline">

                  Feb 1, 2020 1:37 PM in response to Stickman32

              </span>
              <span class="show-tablet-inline">

                  In response to Stickman32

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>Same problem here with a Macbook pro 16 inch i9 after update to catalina 10.15.3.</p><p>SecurityAgent process all night at 100%, for more than 8 hours so it never settle. After reboot the high CPU load is gone.</p><p><br /></p><p>Created a sample of the process (I could not send it in the Feedback to apple because the field isn&#39;t big enough.</p><p><br /></p><div><a href="https://discussions.apple.com/content/attachment/f380cef1-3c22-4b64-a7cb-bf8b361219db" download="Sample of SecurityAgent1.txt.log" rel="nofollow">Sample of SecurityAgent1.txt</a></div><p><br /></p><p>Looks like something to do with display (got an external monitor connected)</p><pre spellcheck="false"><code aria-label="Code">Sort by top of stack, same collapsed (when &gt;&#61; 5):
        __ulock_wait  (in libsystem_kernel.dylib)        2836
        mach_msg_trap  (in libsystem_kernel.dylib)        2836
        CoreDisplay::XXH64(unsigned char const*, unsigned long long)  (in CoreDisplay)        1322
        syscall_thread_switch  (in libsystem_kernel.dylib)        1251
        _platform_memmove$VARIANT$Haswell  (in libsystem_platform.dylib)        218
        GetRealtimeDisplayInfo(unsigned int)  (in CoreDisplay)        39
</code></pre></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Feb 1, 2020 1:37 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=252071336022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=252071336022">Helpful&nbsp;(2)</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;252071336022#252071336022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>




<article





    id="252071606022"
    tabindex="-1"

  class="content-post answer" data-analytics="thread-answer" data-analytics-id="252071606" data-action="thread-reply">



  <div class="header" data-action="content-post-header">











      <div class="post-author-profile author-content">



  <a
    class="user-avatar"


        href="/profile/bvramana"

      data-action="common-user-avatar"
      data-user-id="7ab5cac3ad277a60"


  >

  <span class="a11y">
    User profile for user:

      bvramana

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_8999.png"
  class="avatar-contain default-avatar"
  alt="bvramana"
  aria-hidden="true" />

  </a>



        <div class="post-author-metadata" >
          <a
            class="post-author-name"


                href="/profile/bvramana"

              data-action="content-post-user"
              data-user-id="7ab5cac3ad277a60"

          >
            <span class="author-name" >
              bvramana
            </span>
          </a>

          <span class="post-author-reputation">


  <div class="user-level large"

  >

        <div class="level-image user-level-icon-1" aria-hidden="true"></div>
          <span class="level-label">
            <span class="a11y">User level:</span>
            Level&nbsp;1

    </span>
  </div>




                <span class="points">
                  (4 points)
                </span>



          </span>
        </div>
      </div>







  </div>



  <div class="body">



    <div class="post-content">





        <p class="timestamp timestamp-top">

            <a class="in-response-to" href="/thread/250873047?answerId&#x3D;251909904022#251909904022">
              <span class="hide-tablet-inline">

                  Feb 1, 2020 2:37 PM in response to bvramana

              </span>
              <span class="show-tablet-inline">

                  In response to bvramana

              </span>
            </a>

        </p>




      <div class="post-body" data-action="content-post-body">


        <div data-action="content-post-body-content" class="content-post-body-content" tabindex="-1" data-analytics="content-post:body" ><p>I haven&#39;t observed since last 3 weeks, this issue is gone for now. </p><p><br /></p><p>My fans are always off mostly unless i connect monitor or running some intensive jobs.</p></div>

        <div class="post-content-toggle" data-action="content-post-toggle-area">
          <button class="post-content-toggle-button" data-action="content-post-toggle-button">
            <span class="more-label" aria-label="Show post content">More</span>
            <span class="less-label" aria-label="Hide post content">Less</span>
          </button>
        </div>
      </div>




        <p class="timestamp timestamp-bottom show-tablet">


              Feb 1, 2020 2:37 PM


        </p>


      <div class="action-bar" data-action="content-post-action-bar">







              <a class="button button-black" href="/login?replyId=252071606022" data-analytics="content-post:action:reply:link">Reply</a>


            <a class="button button-white" href="/login?helpfulId=252071606022">Helpful</a>











<div class="dropdown" data-action="content-post-drop-down" data-analytics="content-post:actions:drop-down">





    <button class="button button-white drop-down-button arrow interactive" aria-haspopup="true" aria-expanded="false" data-action="drop-down-button" >
      <span class="icon icon-paddledown"></span>
      <span class="a11y">Thread reply - more options</span>
    </button>












<ul class="drop-down-menu arrow hidden right" data-analytics="content-post:actions:drop-down"   data-action="drop-down-menu" role="menu">

    <li class="menu-item" role="presentation"><a role="menuitem" class="menu-item-link" href="/thread/250873047?answerId&#x3D;252071606022#252071606022" data-action="drop-down-menu-item">Link to this Post</a></li>

</ul>



</div>








      </div>
    </div>
  </div>
</article>






          </div>


              <div class="bottom-pagination">



<nav class="pagination" data-action="pagination" role="navigation" aria-label="Pagination" data-current-page="1" data-total-pages="3">
  <ol class="pagination-list" role="presentation">
    <li>
      <a class="first-page hidden" href="/thread/250873047" aria-label="First page" data-action="pagination-first" role="button">
        first
      </a>
    </li>

    <li>
      <a class="previous-page icon icon-standalone icon-chevronleft hidden" role="button" href="#" aria-label="Previous page" data-action="pagination-prev">
      </a>
    </li>

    <li>
      <span class="page-number" role="text" aria-label="Page 1 of 3">

          <span class="hide-mobile-inline-block" data-action="pagination-page-number-text">
            Page 1 of 3
          </span>
          <span class="hide-desktop-inline-block" data-action="pagination-page-number-text-mobile">
            Page 1/3
          </span>

      </span>
    </li>

    <li>
      <a class="next-page icon icon-standalone icon-chevronright" role="button" data-action="pagination-next" href="?page=2" aria-label="Next page">
      </a>
    </li>


      <li>
        <a class="last-page" href="?page=3" aria-label="Last page" role="button" data-action="pagination-last">
          last
        </a>
      </li>

  </ol>
</nav>



    <div class="pagination-overlay" aria-hidden="true" data-analytics="pagination-overlay">
      <span data-action="pagination-page-number-text-mobile">
        Page 1/3
      </span>
    </div>



              </div>


        </section>


		<section class="persist-question" data-action="persist-question" role="region" aria-label="Question summary" data-analytics-id="250873047">
    <button class="icon icon-close" data-action="persist-question-close" aria-label="Close dialog"></button>
    <div class="content">


  <a
    class="user-avatar"


        href="/profile/admiral+u"

      data-action="common-user-avatar"
      data-user-id="5b8aad917c4b38ea"


  >

  <span class="a11y">
    User profile for user:

      admiral u

  </span>
  <img src="/public/assets/avatars/SYSTEM_DEFAULT_AVATAR_EN_1153.png"
  class="avatar-contain medium-avatar"
  alt="admiral u"
  aria-hidden="true" />

  </a>

      <p class="title">
        <span class="a11y">Question:</span>
        <span class="drop-cap" aria-hidden="true">Q:</span>
        <span data-action="persist-question-text" tabindex="-1" class="persist-question-text">Security Agent causing high cpu</span>
        <button class="persist-question-toggler hidden" data-action="persist-question-toggler">
          <span class="more-label" aria-label="More content">More</span>
          <span class="less-label" aria-label="Less content">Less</span>
        </button>
      </p>
    </div>

  </section>



      </div>
    </main>
    <script src="https://communities.apple.com/en202005220507/public/compiled/pages/thread.js" type="text/javascript" defer></script>



    </div>



    <footer id="ac-globalfooter" lang="en-US" data-analytics-region="global footer" role="contentinfo" aria-labelledby="ac-gf-label">

    <div class="ac-gf-content">

        <h2 class="ac-gf-label" id="ac-gf-label">Apple Footer</h2>

        <section class="ac-gf-sosumi">
            <ul>
                <li>
                    This site contains user submitted content, comments and opinions and is for informational purposes only. Apple may provide or recommend responses as a possible solution based on the information provided; every potential issue may involve several factors not detailed in the conversations captured in an electronic forum and Apple can therefore provide no guarantee as to the efficacy of any proposed solutions on the community forums. Apple disclaims any and all liability for the acts, omissions and conduct of any third parties in connection with or related to your use of the site. All postings and use of the content on this site are subject to the
                    <a href="/terms">Apple Support Communities Terms of Use</a>.
                    <a href="/privacy">See how your data is managed...</a>
                </li>
            </ul>
        </section>

        <nav class="ac-gf-breadcrumbs" aria-label="Breadcrumbs" role="navigation">
            <a href="//www.apple.com" class="home ac-gf-breadcrumbs-home">
                <span class="ac-gf-breadcrumbs-home-icon" aria-hidden="true"></span>
                <span class="ac-gf-breadcrumbs-home-label">Apple</span>
                <span class="ac-gf-breadcrumbs-home-chevron"></span>
                <span class="ac-gf-breadcrumbs-home-mask"></span>
            </a>
            <div class="ac-gf-breadcrumbs-path">
                <ol class="ac-gf-breadcrumbs-list">
                    <li class="ac-gf-breadcrumbs-item">
                        <a class="ac-gf-breadcrumbs-link" href="https://www.apple.com/support/">Support</a>
                    </li>
                    <li class="ac-gf-breadcrumbs-item">
                        <a class="ac-gf-breadcrumbs-link" href="/">Communities</a>
                    </li>
                </ol>
            </div>
        </nav>


        <section class="ac-gf-footer">
            <div class="ac-gf-footer-shop" x-ms-format-detection="none">
                More ways to shop: Visit an <a href="//www.apple.com/retail/">Apple Store</a>, <span class="nowrap">call 1-800-MY-APPLE, or <a href="https://locate.apple.com/">find a reseller</a></span>.
            </div>
            <div class="ac-gf-footer-locale">
                <a class="ac-gf-footer-locale-link" href="/choose-country-region" title="Choose your country or region" aria-label="United States. Choose your country or region"><span class="ac-gf-footer-locale-flag" data-hires="false"></span>United States</a>
            </div>
            <div class="ac-gf-footer-legal">
                <div class="ac-gf-footer-legal-copyright">Copyright © <script>document.write(new Date().getFullYear());</script> Apple Inc. All rights reserved.</div>
                <div class="ac-gf-footer-legal-links">
                    <a class="ac-gf-footer-legal-link" href="//www.apple.com/privacy/privacy-policy/">Privacy Policy</a>
                    <a class="ac-gf-footer-legal-link" href="//www.apple.com/legal/internet-services/terms/site.html">Terms of Use</a>
                    <a class="ac-gf-footer-legal-link" href="//www.apple.com/us/shop/goto/help/sales_refunds">Sales and Refunds</a>
                    <a class="ac-gf-footer-legal-link" href="//www.apple.com/legal/">Legal</a>
                    <a class="ac-gf-footer-legal-link" href="//www.apple.com/sitemap/">Site Map</a>
                </div>
            </div>
        </section>


    </div>
</footer>


    <div class="mobile-search" role="dialog" tabindex="-1">
  <button class="icon icon-close" aria-label="Close" data-action="close-mobile-search"></button>
  <form action="/search" class="search-form-mobile" method="GET" data-action="mobile-search-form" novalidate="novalidate">
    <label for="askaquestion-mobile">Ask a question</label>
    <input type="text" aria-required="true" id="askaquestion-mobile" name="q" required autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" maxlength="250" placeholder="Search or ask a question" aria-invalid="false" data-action="mobile-search" tabindex="0" aria-controls="search-aria-live-mobile">
    <button class="icon icon-close reset-button hidden" data-action="mobile-reset">
      <span class="a11y">Reset</span>
    </button>
  </form>
</div>


    <script>
  var _store = {
    'lang': 'en',
    'basePath': '',
    'cdnPrefix': 'https://communities.apple.com/en202005220507',
    'communityContext': '',
    'token': 'anonymous',
    'user': {
      'loggedIn': 'false' == 'true',
      'userLevel': '',
      'userId': '',
      'nickname': '',
      'url': ''
    },
    'analytics': {
      'pageAnnouncements': ['no announcement']
    },
      '_config': {
        "ui.subNav.corporateLoginEnabled": 'true'
        ,'ui.okapi.enabled': 'false'
        ,'ui.okapi.basePath': ''
        ,'ui.okapi.pixelTest': 'false'
        ,'ui.okapi.projectSlug': 'ASC_Demo'
        ,'ui.okapi.goalName.AB': 'Pixel_test__AB'
        ,'ui.okapi.testSlug.AB': 'Pixel_test__AB'
        ,'ui.okapi.goalName.ABN': 'Pixel_test__ABN'
        ,'ui.okapi.testSlug.ABN': 'Pixel_test__ABN'
        ,'ui.okapi.goalName.AABB': 'Pixel_test__AABB'
        ,'ui.okapi.testSlug.AABB': 'Pixel_test__AABB'
        ,'ui.okapi.testSlug.token.AB': 'd1d40527edef5633ae488de472a66df7'
        ,'ui.okapi.testSlug.token.ABN': '582ce036108caa28a73e10465c224f4b'
        ,'ui.okapi.testSlug.token.AABB': '4240dfbad595e0a7a5fdcc10dfdd0c09'
        ,'ui.okapi.subNav.loginLinkTest': 'false'
        ,'ui.okapi.subNav.loginLinkTest.testSlug': 'Sub_nav_login_link_copy'
        ,'ui.okapi.subNav.loginLinkTest.token': '52e34d55a77241e3ea00edb4f70bb5ef'
        ,'ui.okapi.subNav.loginLinkTest.projectSlug': 'ASC'
        ,'ui.okapi.subNav.loginLinkUsersValidation': 'true'
        ,'ui.okapi.subNav.loginLinkUsersValidation.testSlug': 'Sub_nav_login_link_users_validation'
        ,'ui.okapi.subNav.loginLinkUsersValidation.projectSlug': 'ASC'
        ,'ui.okapi.subNav.loginLinkUsersValidation.token': '9e1ea05af0dbb083c95859234b7b2cf4'




                  ,'ui.okapi.testSlug.threadPage': 'Thread_page_search_widget'
                  ,'ui.okapi.goalName.threadPage': 'search_box_focus'
                  ,'ui.okapi.threadPage.searchWidgetTest': 'false'
                  ,'ui.okapi.threadPage.searchWidgetTest.env': 'phoenix-uat'



          ,"filters.sortBy.urlParam": 'sortBy'

      },
    '_i18n': {
      // Mobile search
      'common.search.searching': 'Searching for similar questions and communities'
      ,'common.search.results.notFound': 'We did not find a similar question in the community'
      ,'common.search.results.submit': 'Ask the community'
      ,'common.search.a11y.tableTitle': '{0} for {1}'
      ,'common.search.results.titles.communities': 'Communities'
      ,'common.search.results.titles.discussions': 'Discussions'
      ,'common.search.results.viewAll': 'We found {0} similar questions'
      ,'common.search.result.view': 'We found 1 similar question'
      ,'common.search.results.by': 'By'
      ,'common.user.defaultNickname': 'Community User'



      // popup
      ,'common.popup.close': 'Close dialog'
      ,'common.user.a11y.closePopup': 'Close user profile'
      ,'common.user.a11y.avatar': 'User avatar'
      ,'common.user.a11y.userInfo': 'User profile information for user:'
      ,'common.user.a11y.level': 'User level:'
      ,'common.user.a11y.userLevel': 'User level:'
      ,'common.user.a11y.user': 'User'
      ,'common.user.a11y.awardAchieved': 'Award achieved'
      ,'common.user.a11y.awardNotAchieved': 'Award not achieved yet'
      ,'common.user.a11y.stepAchieved': 'Step completed'
      ,'common.user.a11y.stepNotAchieved': 'Step not completed yet'
      ,'common.user.a11y.expertiseLevel': 'Speciality level out of ten:'
      ,'mysubscriptions.a11y.subscribedList': 'List of subscribed {0}'
      ,'mysubscriptions.a11y.threadList': 'Threads List'
      ,'common.email': 'Email'
      ,'common.user.points.name': 'points'
      ,'common.user.expertise.name': 'Specialties'
      ,'common.user.expertise.viewAll': 'More specialties'
      ,'common.user.expertise.learnMore': 'Learn about specialties...'
      ,'common.user.awards.name': 'Awards'
      ,'common.user.settings.title': 'Personal Settings'
      ,'common.user.settings.manageSubscriptions': 'My Subscriptions'
      ,'common.user.settings.changePhoto': 'Change photo &amp; avatar'
      ,'common.user.settings.editProfile': 'Edit profile &amp; privacy'
      ,'common.user.settings.preferences': 'Preferences'
      ,'common.user.settings.logOut': 'Log out'
      ,'common.viewProfile': 'View profile'
      ,'common.actions.follow': 'Follow'
      ,'common.actions.following': 'Following'
      ,'link.TSpecialities': '/learn'
      ,'link.TAwards': '/learn'
      ,'common.user.groups.users': 'Level'
      ,'common.user.groups.operations': 'Community Operations'
      ,'common.user.groups.specialists': 'Community Specialist'
      ,'common.user.groups.managers': 'Community Manager'
      ,'common.user.groups.hosts': 'Community Moderator'
      ,'common.user.groups.devOps': 'Community DevOps'
      ,"common.user.a11y.stepCompleted": 'step has been completed {0} out of {1} times'

      // Error
      ,'common.error.serviceDown': 'We encountered an error while loading this data. Please try again later.'
      ,'errorPage.type': ''
      ,'common.error.title': 'We’re sorry.'
      ,'common.error.pageAjaxFailed': 'An error occurred while loading this page. Please reload the page or try again later.'
      ,'common.error.componentAjaxFailed': 'An error occurred while loading this information. Please reload the page or try again later.'

      // Timestamps
      ,'common.timestamp.justNow': 'less than a minute ago'
      ,'common.timestamp.minuteAgo': '1 minute ago'
      ,'common.timestamp.minutesAgo': '{0} minutes ago'
      ,'common.timestamp.hourAgo': '1 hour ago'
      ,'common.timestamp.hoursAgo': '{0} hours ago'
      ,'common.timestamp.dayAgo': '1 day ago'
      ,'common.timestamp.daysAgo': '{0} days ago'
      ,'common.timestamp.weekAgo': '1 week ago'
      ,'common.timestamp.weeksAgo': '{0} weeks ago'
      ,'common.timestamp.monthAgo': '1 month ago'
      ,'common.timestamp.monthsAgo': '{0} months ago'
      ,'common.timestamp.yearAgo': '1 year ago'
      ,'common.timestamp.yearsAgo': '{0} years ago'

      // Aria live
      ,'common.a11y.pageLoading': 'Loading page content'
      ,'common.a11y.pageLoaded': 'Page content loaded'

      // Pagination
      ,'common.pagination.page': 'Page {0}'
      ,'common.pagination.pageOf': 'Page {0} of {1}'
      ,'common.pagination.pageOfMobile': 'Page {0}/{1}'

      // Subcommunity
      ,'subCommunity.leaderBoard.community': ''

      // Filters layout
      ,"common.and": 'and'
      ,"common.listView.a11y.userTipsHeader": 'User Tips'
      ,"common.filters.contentType.discussions": 'Discussions'
      ,"common.filters.contentType.userTips": 'User Tips'











      ,"common.filters.a11y.filterAuthor": '{0} author choices available'
      ,"common.filters.a11y.noFilterAuthor": 'No users found'
      ,"common.nav.signIn": 'Sign in'
      ,"common.nav.signIn.corporate": 'Sign in corporate'

      // Post Creation
      ,"createPost.post.body.placeholder": 'Have a question or something to share? Start a conversation with the community.'
      ,"createPost.select.a11y": 'You’ve selected {0}'
      ,"createPost.notification.text": 'We saved the content from your last session.'
      ,"createPost.notification.link": 'Start this post where you left off.'
    },
    i18n: function(key) {
      if (key === 'all') return this._i18n;
      else if (this._i18n[key]) return this._i18n[key];
      return key;
    },
    config: function(key) {
      if (key === 'all') return this._config;
      else if (this._config[key]) return this._config[key];
      return key;
    }
  };
</script>




    <script src="https://communities.apple.com/en202005220507/public/scripts/dtml.js" type="text/javascript"></script>
    <script src="https://communities.apple.com/en202005220507/public/compiled/decorator.js" type="text/javascript" defer></script>
    <script type="text/javascript" async src="//communities.apple.com/ac20190730/globalnav/4/en_US/scripts/ac-globalnav.built.js"></script>
  </body>
</html>
"""
