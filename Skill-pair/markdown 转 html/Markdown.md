<!DOCTYPE html>
<html itemscope itemtype="http://schema.org/WebPage">
<head>
<title>Markdown</title>
<meta itemprop="name" content="Markdown"/>
<meta name="twitter:title" content="Markdown"/>
<meta name="og:title" content="Markdown"/>
<meta itemprop="description" content="Markdown syntax reference, as understood by the TAG Neuron."/>
<meta name="twitter:description" content="Markdown syntax reference, as understood by the TAG Neuron."/>
<meta name="og:description" content="Markdown syntax reference, as understood by the TAG Neuron."/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="Markdown syntax reference, as understood by the TAG Neuron. Author: Peter Waher, Date: 2016-02-11"/>
<meta name="author" content="Peter Waher"/>
<link rel="copyright" href="/Copyright.md"/>
<link rel="shortcut icon" href="/favicon.ico"/>
<link rel="stylesheet" href="/Themes/WinterDawn/WinterDawn.cssx"/>
<script type="application/javascript" src="/Master.js"></script>
<script type="application/javascript" src="/Events.js"></script>
<link rel="stylesheet" href="/highlight/styles/default.css">
<script src="/highlight/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
</head>
<body>
<p><header id="native-header">
<nav>
<div>
<button id="toggle-nav" onClick="NativeHeader.ToggleNav()">☰</button>
<p id="small-pagpage-name">
<strong>Markdown</strong>
</p>
</div>
<ul>
<li><a href="/Welcome.md">Home</a></li>
<li><a href="https://www.trustanchorgroup.com/" target="_blank">TAG</a></li>
<li><a href="https://abc4.io/" target="_blank">ABC4.IO</a></li>
<li><a href="https://lils.is/" target="_blank">LILS.IS</a></li>
<li><p id="large-pagpage-name">Markdown</p></li>
<li><a href="https://www.linkedin.com/in/peterwaher" target="_blank">LinkedIn</a></li>
<li><a href="https://twitter.com/PeterWaher" target="_blank">Twitter</a></li>
<li><a href="https://waher.se/Feedback.md" target="_blank">Feedback</a> </nav> </header> <main></li>
</ul>
</p>
<section>
<h1 id="markdownSyntaxReference" class="tocReference">Markdown syntax reference</h1>
<p><em>Markdown</em> is a very simple, yet efficient format for editing text-based content. The <strong>TAG Neuron</strong> converts Markdown to HTML automatically  when web browsers download it, making it a powerful tool for publishing online content. The syntax is inspired by the  <a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">original markdown syntax</a> as defined by John Gruber at Daring Fireball, but contains  numerous other additions and modifications. Some of these are introduced in the <strong>TAG Neuron</strong>, others are inspired by selected features used  in <a href="https://rawgit.com/fletcher/human-markdown-reference/master/index.html" target="_blank">MultiMarkdown</a> and  <a href="https://michelf.ca/projects/php-markdown/extra/" target="_blank">Markdown Extra</a>. Below, is a summary of the markdown syntax, as understood by the <strong>TAG Neuron</strong>.</p>
<p><strong>Note</strong>: You can use the <a href="MarkdownLab/MarkdownLab.md">Markdown Lab</a> to experiment with Markdown syntax.</p>
<div class="toc">
<div class="tocTitle">Table of Contents</div><div class="tocBody">
<ol>
<li><a href="#inlineConstructs">Inline constructs</a><ol>
<li><a href="#textFormatting">Text formatting</a><ol>
<li><a href="#emphasizedText">Emphasized text</a></li>
<li><a href="#strongText">Strong text</a></li>
<li><a href="#underlinedText">Underlined text</a></li>
<li><a href="#superscriptText">Superscript text</a></li>
<li><a href="#subscript">Subscript</a></li>
<li><a href="#insertedText">Inserted text</a></li>
<li><a href="#strikethroughText">Strikethrough text</a></li>
<li><a href="#deletedText">Deleted text</a></li>
<li><a href="#inlineCode">Inline code</a></li></ol></li>
<li><a href="#links">Links</a><ol>
<li><a href="#shorthandLinks">Shorthand links</a></li>
<li><a href="#automaticWebLinks">Automatic web links</a></li>
<li><a href="#abbreviations">Abbreviations</a></li>
<li><a href="#hashtags">Hashtags</a></li></ol></li>
<li><a href="#inlineHtml">Inline HTML</a></li>
<li><a href="#specialCharactersInHtml">Special characters in HTML</a></li>
<li><a href="#escapeCharacter">Escape character</a></li>
<li><a href="#typographicalEnhancements">Typographical enhancements</a></li>
<li><a href="#emojis">Emojis</a></li>
<li><a href="#smileys">Smileys</a></li>
<li><a href="#htmlEntities">HTML Entities</a></li></ol></li>
<li><a href="#blockConstructs">Block constructs</a><ol>
<li><a href="#paragraphs">Paragraphs</a></li>
<li><a href="#lineBreaks">Line breaks</a></li>
<li><a href="#headers">Headers</a></li>
<li><a href="#blockQuotes">Block quotes</a></li>
<li><a href="#bulletLists">Bullet Lists</a></li>
<li><a href="#numberedLists">Numbered Lists</a></li>
<li><a href="#definitionLists">Definition Lists</a></li>
<li><a href="#taskLists">Task lists</a></li>
<li><a href="#horizontalAlignmentOfText">Horizontal Alignment of text</a><ol>
<li><a href="#leftAlignmentOfText">Left alignment of text</a><ol>
<li><a href="#leftAlignedExample">Left-aligned Example</a></li></ol></li>
<li><a href="#rightAlignmentOfText">Right alignment of text</a><ol>
<li><a href="#rightAlignedExample">Right-aligned Example</a></li></ol></li>
<li><a href="#centerAlignmentOfText">Center alignment of text</a><ol>
<li><a href="#centerAlignedExample">Center-aligned Example</a></li></ol></li>
<li><a href="#marginAlignmentOfText">Margin alignment of text</a><ol>
<li><a href="#marginAlignedExample">Margin-aligned Example</a></li></ol></li></ol></li>
<li><a href="#codeBlocks">Code blocks</a><ol>
<li><a href="#indentationOfHtml">Indentation of HTML</a></li>
<li><a href="#2dLayoutDiagrams">2D Layout diagrams</a></li>
<li><a href="#graphvizDiagrams">GraphViz diagrams</a></li>
<li><a href="#umlWithPlantuml">UML with PlantUML</a></li>
<li><a href="#embedInlineImages">Embed inline images</a></li>
<li><a href="#embedPdfDocuments">Embed PDF documents</a></li></ol></li>
<li><a href="#comments">Comments</a></li>
<li><a href="#horizontalRules">Horizontal rules</a></li>
<li><a href="#sections">Sections</a></li>
<li><a href="#invisibleBreaks">Invisible breaks</a></li>
<li><a href="#footnotes">Footnotes</a></li>
<li><a href="#tables">Tables</a></li>
<li><a href="#blockLevelHtml">Block-level HTML</a></li></ol></li>
<li><a href="#multimedia">Multimedia</a><ol>
<li><a href="#images">Images</a></li>
<li><a href="#video">Video</a></li>
<li><a href="#audio">Audio</a></li>
<li><a href="#youtube">YouTube</a></li>
<li><a href="#externalWebPage">External web page</a></li>
<li><a href="#tableOfContents">Table of Contents</a></li>
<li><a href="#markdownInclusion">Markdown inclusion</a></li></ol></li>
<li><a href="#script">Script</a><ol>
<li><a href="#inlineScript">Inline script</a><ol>
<li><a href="#graphs">Graphs</a></li></ol></li>
<li><a href="#preProcessedScript">Pre-processed script</a><ol>
<li><a href="#loopsAndDynamicContent">Loops and dynamic content</a></li></ol></li>
<li><a href="#asynchronousProcessingOfScript">Asynchronous processing of script</a></li>
<li><a href="#sessionsAndVariables">Sessions and variables</a></li>
<li><a href="#queryParameters">Query parameters</a></li>
<li><a href="#globalVariables">Global variables</a></li>
<li><a href="#pageLocalVariables">Page-local variables</a></li>
<li><a href="#currentRequest">Current request</a></li>
<li><a href="#currentResponse">Current response</a></li>
<li><a href="#postedData">Posted data</a></li>
<li><a href="#webServices">Web Services</a><ol>
<li><a href="#webScript">Web Script</a></li>
<li><a href="#markdownBasedServices">Markdown-based Services</a></li></ol></li>
<li><a href="#generationOfJavascript">Generation of JavaScript</a><ol>
<li><a href="#generatedJavascriptExample">Generated JavaScript Example</a></li></ol></li></ol></li>
<li><a href="#metadata">Metadata</a><ol>
<li><a href="#allowscripttag">AllowScriptTag</a></li>
<li><a href="#alternate">Alternate</a></li>
<li><a href="#audioautoplay">AudioAutoplay</a></li>
<li><a href="#audiocontrols">AudioControls</a></li>
<li><a href="#author">Author</a></li>
<li><a href="#bodyonly">BodyOnly</a></li>
<li><a href="#copyright">Copyright</a></li>
<li><a href="#css">CSS</a></li>
<li><a href="#date">Date</a></li>
<li><a href="#description">Description</a></li>
<li><a href="#details">Details</a></li>
<li><a href="#help">Help</a></li>
<li><a href="#icon">Icon</a></li>
<li><a href="#image">Image</a></li>
<li><a href="#init">Init</a></li>
<li><a href="#javascript">JavaScript</a></li>
<li><a href="#keywords">Keywords</a></li>
<li><a href="#login">Login</a></li>
<li><a href="#master">Master</a></li>
<li><a href="#next">Next</a></li>
<li><a href="#parameter">Parameter</a></li>
<li><a href="#previousOrPrev">Previous or Prev</a></li>
<li><a href="#privilege">Privilege</a></li>
<li><a href="#refresh">Refresh</a></li>
<li><a href="#script">Script</a></li>
<li><a href="#subtitle">Subtitle</a></li>
<li><a href="#title">Title</a></li>
<li><a href="#uservariable">UserVariable</a></li>
<li><a href="#videoautoplay">VideoAutoplay</a></li>
<li><a href="#videocontrols">VideoControls</a></li>
<li><a href="#viewport">Viewport</a></li>
<li><a href="#web">Web</a></li></ol></li>
<li><a href="#httpHeaderFields">HTTP Header Fields</a><ol>
<li><a href="#accessControlAllowOrigin">Access-Control-Allow-Origin</a></li>
<li><a href="#cacheControl">Cache-Control</a></li>
<li><a href="#contentSecurityPolicy">Content-Security-Policy</a></li>
<li><a href="#publicKeyPins">Public-Key-Pins</a></li>
<li><a href="#strictTransportSecurity">Strict-Transport-Security</a></li>
<li><a href="#sunset">Sunset</a></li>
<li><a href="#vary">Vary</a></li></ol></li></ol>
</div>
</div>
</section>
<section>
<h2 id="inlineConstructs" class="tocReference">Inline constructs</h2>
<p>Markdown includes a series of simple syntax constructs, categorized into different types. Inline constructs are constructs that can be used in normal text flow. The follow subsections show available inline constructs that can be used to enhance the text.</p>
<h3 id="textFormatting" class="tocReference">Text formatting</h3>
<p>In Markdown it&rsquo;s easy to format text. Special characters are used around the text you want to format, as is shown in the following subsections.</p>
<h4 id="emphasizedText" class="tocReference">Emphasized text</h4>
<p>To emphasize text, enclose the text using asterisks <code>*</code>, such as this: <code>*Emphasized text*</code>. In HTML, this becomes: <em>Emphasized text</em>. Emphasized text  can be included in the <em>middle</em> of a sentance, or in the mi<em>dd</em>le of a word. In HTML, emphasized text gets surrounded by <code>&lt;em&gt;</code> and <code>&lt;/em&gt;</code> tags.</p>
<h4 id="strongText" class="tocReference">Strong text</h4>
<p>Strong text is included by surrounding it with double asterisks <code>**</code>. Example: <code>**Strong text**</code>. Result: <strong>Strong text</strong>. As with emphasized text,  it can be included in the <strong>middle</strong> of a sentance, or in the mi<strong>dd</strong>le of a word. In HTML, strong text gets surrounded by <code>&lt;strong&gt;</code> and <code>&lt;/strong&gt;</code> tags.</p>
<h4 id="underlinedText" class="tocReference">Underlined text</h4>
<p>Underlined text is created by surrounding the underlined text with underscores <code>_</code>. Example: <code>_Underlined text_</code>. This is transformed to:  <u>Underlined text</u>. As with other text formatting operators, underlined text can be included in the <u>middle</u> of a sentance, or in the mi<u>dd</u>le of a word. In HTML, underlined text gets surrounded by <code>&lt;u&gt;</code> and <code>&lt;/u&gt;</code> tags.</p>
<h4 id="superscriptText" class="tocReference">Superscript text</h4>
<p>You can add superscript text by inserting the superscript text between a <code>^[</code> and a <code>]</code>, or a <code>^(</code> and a <code>)</code>. If you want to use parenthesis <code>(</code> or <code>)</code> in your superscript text, you should use <code>^[</code> and <code>]</code>. You could also escape the parenthesis using <code>\(</code> or <code>\)</code>. Some special characters, like the digits and ASCII letters can superseed the <code>^</code> sign without having to be enclosed in parenthesis or brackets. See  <a href="#typographicalEnhancements">Typographical enhancements</a> for details.</p>
<p>Examples: </p>
<ul>
<li><code>Some^[superscript]</code> &rArr; Some<sup>superscript</sup></li>
<li><code>a^[b+c]=a^ba^c</code> &rArr; a<sup>b+c</sup>=a<sup>b</sup>a<sup>c</sup></li>
<li><code>a^2+b^2=c^2</code> &rArr; a&#178;+b&#178;=c&#178;</li>
<li><code>a^n+b^n&lt;&gt;c^n, n&gt;=3</code> &rArr; a<sup>n</sup>+b<sup>n</sup>&ne;c<sup>n</sup>, n&geq;3</li>
<li><code>a^[(b+c)/2]=sqrt(a^ba^c)</code> &rArr; a<sup>(b+c)/2</sup>=sqrt(a<sup>b</sup>a<sup>c</sup>)</li>
<li><code>a^(\(b+c\)/2)=sqrt(a^ba^c)</code> &rArr; a<sup>(b+c)/2</sup>=sqrt(a<sup>b</sup>a<sup>c</sup>)</li>
</ul>
<h4 id="subscript" class="tocReference">Subscript</h4>
<p>Text between brackets <code>[</code> and <code>]</code>, that do not form part of a link, a link reference, reference definitions or a multi-media definition or reference,  is treated as subscript text. Examples:</p>
<ul>
<li><code>Some[subscript]</code> &rArr; Some<sub>subscript</sub></li>
<li><code>a[i]=A[i,j]</code> &rArr; a<sub>i</sub>=A<sub>i,j</sub></li>
</ul>
<h4 id="insertedText" class="tocReference">Inserted text</h4>
<p>Inserted text, which by default is also shown as underlined (but which can be changed to a different style using style sheets), is created by surrounding  the inserted text with double underscores <code>__</code>. Example: <code>__Inserted text__</code>. This becomes: <ins>Inserted text</ins>. As with the operators above, inserted text  can be included in the <ins>middle</ins> of a sentance  or in the mi<ins>dd</ins>le of a word. In HTML, inserted text gets surrounded by <code>&lt;ins&gt;</code> and <code>&lt;/ins&gt;</code> tags.</p>
<h4 id="strikethroughText" class="tocReference">Strikethrough text</h4>
<p>Strikethrough text is created by surrounding its text using tildes <code>~</code>. Example: <code>~Strikethrough text~</code>. This is transformed to: <s>Strikethrough text</s>.  As with the other text formatting operators, it can be included in the <s>middle</s> of a sentance or in the mi<s>dd</s>le of a word. In HTML, strikethrough text  gets surrounded by <code>&lt;s&gt;</code> and <code>&lt;/s&gt;</code> tags.</p>
<h4 id="deletedText" class="tocReference">Deleted text</h4>
<p>Deleted text, which by default is also shown as strikethrough text (but which can be changed to a different style using style sheets), is created by  surrounding the inserted text with double tildes <code>~~</code>. Example: <code>~~Deleted text~~</code>- Result: <del>Deleted text</del>. As with the operators above, deleted text  can be included in the <del>middle</del> of a sentance or in the mi<del>dd</del>le of a word. In HTML, inserted text gets surrounded by <code>&lt;del&gt;</code> and <code>&lt;/del&gt;</code> tags.</p>
<h4 id="inlineCode" class="tocReference">Inline code</h4>
<p>Inline code can be used to include code into flowing text. To include inline code, surround it using single or double back ticks <code>`</code>, as shown in the  following example: <code>`Inline code`</code>. This is transformed to: <code>Inline code</code>. As with other text formatting operators, inline code can be included in the  <code>middle</code> of a sentance or in the mi<code>dd</code>le of a word. In HTML, inserted text gets surrounded by <code>&lt;code&gt;</code> and <code>&lt;/code&gt;</code> tags.</p>
<p><strong>Note</strong>: Characters that have special meaning in markdown, such as *, _, ~, etc., are shown as normal characters in inline code.</p>
<p><strong>Note 2</strong>: If you want to include a back tick in the inline code, you can surround the inline code using double back ticks and a space, one after the first double back tick, and one before the last back tick, such as this: <code>`` `Inline code` ``</code>. This sequence was used to produce <code>`Inline code`</code>.</p>
<h3 id="links" class="tocReference">Links</h3>
<p>To include a link into a markdown text, you can, apart from automatic links, also include custom links. These are written in the form <code>[Text](URL)</code> or <code>[Text](URL "Title")</code>. The text can include inline formatting, if desired. URLs can be absolute (include URI scheme) or local relative links (without URI scheme).</p>
<p>Some examples:</p>
<table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:left"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left">Markdown</th>
<th style="text-align:left">Result</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left"><code>[An example](http://example.com/)</code></td>
<td style="text-align:left"><a href="http://example.com/" target="_blank">An example</a></td>
</tr>
<tr>
<td style="text-align:left"><code>[An example](http://example.com/ "Example link")</code></td>
<td style="text-align:left"><a href="http://example.com/" title="Example link" target="_blank">An example</a></td>
</tr>
<tr>
<td style="text-align:left"><code>[A *local* link](/Index.md "Local link back to the main page.")</code></td>
<td style="text-align:left"><a href="/Index.md" title="Local link back to the main page.">A <em>local</em> link</a></td>
</tr>
</tbody>
</table>
<p>To facilitate writing text, and reusing links, it&rsquo;s possible to use a reference instead of a direct URL in the link definition. This is done using  brackets instead of parenthesis, with an optional space between the two sections, and a reference ID instead of the URL, as this: <code>[Text][Reference]</code> or <code>[Text] [Reference]</code>. References are case insensitive. It&rsquo;s also possible to use an implicit reference identity. In this case, the second set of brackets  is empty. The reference identity is taken to be the same as the text for the link.</p>
<table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:left"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left">Markdown</th>
<th style="text-align:left">Result</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left"><code>[An example][EX]</code></td>
<td style="text-align:left"><a href="http://example.com/" target="_blank">An example</a></td>
</tr>
<tr>
<td style="text-align:left"><code>[An example] [ex]</code></td>
<td style="text-align:left"><a href="http://example.com/" target="_blank">An example</a></td>
</tr>
<tr>
<td style="text-align:left"><code>[Example 1][]</code></td>
<td style="text-align:left"><a href="http://example.com/" title="Example 1" target="_blank">Example 1</a></td>
</tr>
<tr>
<td style="text-align:left"><code>[Example 2][]</code></td>
<td style="text-align:left"><a href="http://example.com/" title="Example 2" target="_blank">Example 2</a></td>
</tr>
<tr>
<td style="text-align:left"><code>[Example 3][3]</code></td>
<td style="text-align:left"><a href="http://example.com/" title="Example 3" target="_blank">Example 3</a></td>
</tr>
</tbody>
</table>
<p>The references can then be written anywhere in the document (apart from other text). There are various ways to writing link references. They begin on separate rows, and start with a the reference ID between brackets followed by a colon and then the link <code>[ID]: URL</code>. Optionally, the URL can be surrounded by angle brackets, as follows: <code>[ID]: &lt;URL&gt;</code>. The reference can also have an optional title. This title can follow the URL directly, or be written on the  following row: <code>[ID]: URL "Title"</code>. The title can be surounded between double quotes <code>"Title"</code>, single quotes <code>'Title'</code> or parenthesis <code>(Title)</code>, the  choice is up to the writer. While the references are visible in the markdown document, they will be removed, and not displayed in the generated HTML page.</p>
<p>The following list shows some examples. These examples are used above to create the links in the table.</p>
<pre><code class="nohighlight">[EX]: http://example.com/
[Example 1]: http://example.com/ "Example 1"
[ExAMPLE 2]: &lt;http://example.com/&gt; 'Example 2'
[3]: http://example.com/
	(Example 3)
</code></pre>
<h4 id="shorthandLinks" class="tocReference">Shorthand links</h4>
<p>Markdown help you include links to online resources (URLs) or mail addresses automatically by surrounding them with <code>&lt;</code> and <code>&gt;</code> characters, such as  <code>&lt;http://example.com/&gt;</code> or <code>&lt;address@example.com&gt;</code>. These would turn into clickable links in the HTML representation, as follows: <a href="http://example.com/" target="_blank">http://example.com/</a>  and <a href="&#x6D;&#x61;&#x69;&#x6C;&#x74;&#x6F;&#x3A;&#x61;&#x64;&#x64;&#x72;&#x65;&#x73;&#x73;&#x40;&#x65;&#x78;&#x61;&#x6D;&#x70;&#x6C;&#x65;&#x2E;&#x63;&#x6F;&#x6D;">&#x61;&#x64;&#x64;&#x72;&#x65;&#x73;&#x73;&#x40;&#x65;&#x78;&#x61;&#x6D;&#x70;&#x6C;&#x65;&#x2E;&#x63;&#x6F;&#x6D;</a>.</p>
<p><strong>Note</strong>: It&rsquo;s important to include the <em>URI Scheme</em> (for example <code>http://</code>) in links or the @ sign in mail addresses, for the parser to understand it&rsquo;s  an automatic link or an address, and not another type of construct.</p>
<h4 id="automaticWebLinks" class="tocReference">Automatic web links</h4>
<p>The Markdown parser will create automatic links if your link is a web link, i.e. if it starts with <code>http://</code> or <code>https://</code>. Example:</p>
<pre><code class="nohighlight">http://waher.se/
</code></pre>
<p>Simply becomes:</p>
<p><a href="http://waher.se/" target="_blank">http://waher.se/</a></p>
<p><strong>Note</strong>: Some of the multi-media interfaces supported, can also manage automatic links. If you include a web link that such a multimedia interface recognizes, the corresponding presentation will be used.</p>
<h4 id="abbreviations" class="tocReference">Abbreviations</h4>
<p>You can define abbreviations in your text by writing links using the predefined <code>abbr</code> URI schema, as follows:</p>
<pre><code class="nohighlight">[LOL](abbr:Laugh out Loud) and [OMG](abbr:Oh My God) are two abbreviations commonly used in social networks.
</code></pre>
<p>Result:</p>
<p><abbr data-title="Laugh&nbsp;out&nbsp;Loud">LOL</abbr> and <abbr data-title="Oh&nbsp;My&nbsp;God">OMG</abbr> are two abbreviations commonly used in social networks.</p>
<p><strong>Note</strong>: In <abbr data-title="Hyper&nbsp;Text&nbsp;Markup&nbsp;Language">HTML</abbr>, the <code>&lt;abbr&gt;</code> tag is used. Instead of using the <code>title</code> attribute to present the definition, the <code>data-title</code> attribute is used. This allows the web designer to define how to present the definition, using CSS.</p>
<h4 id="hashtags" class="tocReference">Hashtags</h4>
<p>You can create <mark>hashtags</mark> in markdown by adding a hash character (<code>#</code>) followed by a sequence of letters and/or numbers. No space characters or punctuation marks are allowed. The main function of hashtags is to highlight keywords in a text. Applications can also use them to create  spceial types of links. How such a link would work, is application-specific however, if it exists.</p>
<p>Example: <code>#hashtag</code> becomes <mark>hashtag</mark>.</p>
<h3 id="inlineHtml" class="tocReference">Inline HTML</h3>
<p>Inline HTML elements can be inserted anywhere in markdown text, by just writing it. It can be freely combined with  other inline markdown constructs. Example: <code>This text is &lt;span style='color:#D83134'&gt;colored and **bold**&lt;/span&gt;</code>. This is  transformed into: This text is <span style='color:#D83134'>colored and <strong>bold</strong></span>. You can also use <a href="Entities.md">HTML entities</a>  directly in markdown. For example <code>&amp;copy;</code> is transformed into &copy;.</p>
<p><strong>Note</strong>: Care has to be taken so that the end result is HTML compliant. While HTML can be inserted anywhere, it&rsquo;s only  useful if the markdown is used to generate HTML pages. If the markdown is used to generate other types of content, such  as XAML, inline HTML will be omitted. Since inline HTML is used within block constructs, only span-level HTML constructs  should be used.</p>
<h3 id="specialCharactersInHtml" class="tocReference">Special characters in HTML</h3>
<p>In HTML, certain characters are used to define certain constructs. This includes <code>&lt;</code>, <code>&gt;</code> and <code>&amp;</code>. In markdown, you don&rsquo;t have to escape these, unless they form part of a markdown construct, an HTML tag or an HTML entity. In all other cases, the markdown parser will escape them for you. So, you can write things such as &ldquo;4&lt;5&rdquo;, and &ldquo;AT&amp;T", without having to escape the &lt; into <code>&amp;lt;</code> and the &amp; into <code>&amp;amp;</code>.</p>
<h3 id="escapeCharacter" class="tocReference">Escape character</h3>
<p>If you want to use a character that otherwise has a special funcion in markdown, you can escape it with the backslash character <code>\</code>, to avoid it being interpreted as a control character. If you want to include a backslash character in your text, you need to escape it also, and write two <code>\\</code>.</p>
<p>The following table lists supported escape sequences. Characters not listed in this table do not need to be escaped.</p>
<table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Result</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Result</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Result</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Result</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Result</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><code>\*</code></td>
<td style="text-align:center">*</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\{</code></td>
<td style="text-align:center">{</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\)</code></td>
<td style="text-align:center">)</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\-</code></td>
<td style="text-align:center">-</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\%</code></td>
<td style="text-align:center">%</td>
</tr>
<tr>
<td style="text-align:center"><code>\_</code></td>
<td style="text-align:center">_</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\}</code></td>
<td style="text-align:center">}</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\&lt;</code></td>
<td style="text-align:center">&lt;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\.</code></td>
<td style="text-align:center">.</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\=</code></td>
<td style="text-align:center">=</td>
</tr>
<tr>
<td style="text-align:center"><code>\~</code></td>
<td style="text-align:center">~</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\[</code></td>
<td style="text-align:center">[</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\&gt;</code></td>
<td style="text-align:center">&gt;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\!</code></td>
<td style="text-align:center">!</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\:</code></td>
<td style="text-align:center">:</td>
</tr>
<tr>
<td style="text-align:center"><code>\\</code></td>
<td style="text-align:center">\</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\]</code></td>
<td style="text-align:center">]</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\#</code></td>
<td style="text-align:center">#</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\"</code></td>
<td style="text-align:center">"</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\&#124;</code></td>
<td style="text-align:center">&#124;</td>
</tr>
<tr>
<td style="text-align:center"><code>\</code> <code></code></td>
<td style="text-align:center">`</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\(</code></td>
<td style="text-align:center">(</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\+</code></td>
<td style="text-align:center">+</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>\^</code></td>
<td style="text-align:center">^</td>
<td style="text-align:left"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
</tbody>
</table>
<p><strong>Note</strong>: Some characters only have special meaning in certain situations, such as the parenthesis, brackets, etc. The occurrence of such a character in any other situation does not require escaping.</p>
<h3 id="typographicalEnhancements" class="tocReference">Typographical enhancements</h3>
<p>There are numerous typographical enhancements added to the markdown parser. This makes it easier to generate beautiful text. Some of these additions are are inspired by the the <a href="http://daringfireball.net/projects/smartypants/" target="_blank">Smarty Pants</a> addition to the original markdown, but numerous other character  sequences have been added to the <strong>TAG Neuron</strong> version of markdown, as shown in the following table:</p>
<table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Becomes</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Becomes</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Becomes</th>
<th style="text-align:left"><span style='width:30px'></span></th>
<th style="text-align:center">Sequence</th>
<th style="text-align:center">Becomes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><code>...</code></td>
<td style="text-align:center">&hellip;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>-+</code></td>
<td style="text-align:center">&MinusPlus;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^l</code></td>
<td style="text-align:center"><sup>l</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^L</code></td>
<td style="text-align:center"><sup>L</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>"text"</code></td>
<td style="text-align:center">&ldquo;text&rdquo;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>&lt;&gt;</code></td>
<td style="text-align:center">&ne;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^m</code></td>
<td style="text-align:center"><sup>m</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^M</code></td>
<td style="text-align:center"><sup>M</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>'text'</code></td>
<td style="text-align:center">&lsquo;text&rsquo;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>&lt;=</code></td>
<td style="text-align:center">&leq;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^n</code></td>
<td style="text-align:center"><sup>n</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^N</code></td>
<td style="text-align:center"><sup>N</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>--</code></td>
<td style="text-align:center">&ndash;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>&gt;=</code></td>
<td style="text-align:center">&geq;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^o</code></td>
<td style="text-align:center">&ordm;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^O</code></td>
<td style="text-align:center"><sup>O</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>---</code></td>
<td style="text-align:center">&mdash;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>==</code></td>
<td style="text-align:center">&equiv;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^p</code></td>
<td style="text-align:center"><sup>p</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^P</code></td>
<td style="text-align:center"><sup>P</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(c)</code></td>
<td style="text-align:center">&copy;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^0</code></td>
<td style="text-align:center">&deg;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^q</code></td>
<td style="text-align:center"><sup>q</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^Q</code></td>
<td style="text-align:center"><sup>Q</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(C)</code></td>
<td style="text-align:center">&COPY;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^1</code></td>
<td style="text-align:center">&#185;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^r</code></td>
<td style="text-align:center"><sup>r</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^R</code></td>
<td style="text-align:center"><sup>R</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(r)</code></td>
<td style="text-align:center">&reg;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^2</code></td>
<td style="text-align:center">&#178;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^s</code></td>
<td style="text-align:center"><sup>s</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^S</code></td>
<td style="text-align:center"><sup>S</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(R)</code></td>
<td style="text-align:center">&REG;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^3</code></td>
<td style="text-align:center">&#179;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^t</code></td>
<td style="text-align:center"><sup>t</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^T</code></td>
<td style="text-align:center"><sup>T</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(p)</code></td>
<td style="text-align:center">&copysr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^4</code></td>
<td style="text-align:center"><sup>4</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^u</code></td>
<td style="text-align:center"><sup>u</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^U</code></td>
<td style="text-align:center"><sup>U</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(P)</code></td>
<td style="text-align:center">&copysr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^5</code></td>
<td style="text-align:center"><sup>5</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^v</code></td>
<td style="text-align:center"><sup>v</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^V</code></td>
<td style="text-align:center"><sup>V</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(s)</code></td>
<td style="text-align:center">&oS;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^6</code></td>
<td style="text-align:center"><sup>6</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^w</code></td>
<td style="text-align:center"><sup>w</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^W</code></td>
<td style="text-align:center"><sup>W</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>(S)</code></td>
<td style="text-align:center">&circledS;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^7</code></td>
<td style="text-align:center"><sup>7</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^x</code></td>
<td style="text-align:center"><sup>x</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^X</code></td>
<td style="text-align:center"><sup>X</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>&lt;&lt;</code></td>
<td style="text-align:left"></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^8</code></td>
<td style="text-align:center"><sup>8</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^y</code></td>
<td style="text-align:center"><sup>y</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^Y</code></td>
<td style="text-align:center"><sup>Y</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>&gt;&gt;</code></td>
<td style="text-align:right"></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^9</code></td>
<td style="text-align:center"><sup>9</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^z</code></td>
<td style="text-align:center"><sup>z</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^Z</code></td>
<td style="text-align:center"><sup>Z</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>&lt;&lt;&lt;</code></td>
<td style="text-align:left">&lt;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^a</code></td>
<td style="text-align:center">&ordf;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^A</code></td>
<td style="text-align:center"><sup>A</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^TM</code></td>
<td style="text-align:center">&trade;</td>
</tr>
<tr>
<td style="text-align:center"><code>&gt;&gt;&gt;</code></td>
<td style="text-align:right">&gt;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^b</code></td>
<td style="text-align:center"><sup>b</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^B</code></td>
<td style="text-align:center"><sup>B</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^st</code></td>
<td style="text-align:center"><sup>st</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>&lt;--</code></td>
<td style="text-align:center">&larr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^c</code></td>
<td style="text-align:center"><sup>c</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^C</code></td>
<td style="text-align:center"><sup>C</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^nd</code></td>
<td style="text-align:center"><sup>nd</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>--&gt;</code></td>
<td style="text-align:center">&rarr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^d</code></td>
<td style="text-align:center"><sup>d</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^D</code></td>
<td style="text-align:center"><sup>D</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^rd</code></td>
<td style="text-align:center"><sup>rd</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>&lt;--&gt;</code></td>
<td style="text-align:center">&harr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^e</code></td>
<td style="text-align:center"><sup>e</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^E</code></td>
<td style="text-align:center"><sup>E</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^th</code></td>
<td style="text-align:center"><sup>th</sup></td>
</tr>
<tr>
<td style="text-align:center"><code>&lt;==</code></td>
<td style="text-align:center">&lArr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^f</code></td>
<td style="text-align:center"><sup>f</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^F</code></td>
<td style="text-align:center"><sup>F</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>%0</code></td>
<td style="text-align:center">&permil;</td>
</tr>
<tr>
<td style="text-align:center"><code>==&gt;</code></td>
<td style="text-align:center">&rArr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^g</code></td>
<td style="text-align:center"><sup>g</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^G</code></td>
<td style="text-align:center"><sup>G</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>%00</code></td>
<td style="text-align:center">&pertenk;</td>
</tr>
<tr>
<td style="text-align:center"><code>&lt;==&gt;</code></td>
<td style="text-align:center">&hArr;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^h</code></td>
<td style="text-align:center"><sup>h</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^H</code></td>
<td style="text-align:center"><sup>H</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
<tr>
<td style="text-align:center"><code>[[</code></td>
<td style="text-align:center">&LeftDoubleBracket;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^i</code></td>
<td style="text-align:center"><sup>i</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^I</code></td>
<td style="text-align:center"><sup>I</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
<tr>
<td style="text-align:center"><code>]]</code></td>
<td style="text-align:center">&RightDoubleBracket;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^j</code></td>
<td style="text-align:center"><sup>j</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^J</code></td>
<td style="text-align:center"><sup>J</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
<tr>
<td style="text-align:center"><code>+-</code></td>
<td style="text-align:center">&PlusMinus;</td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^k</code></td>
<td style="text-align:center"><sup>k</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"><code>^K</code></td>
<td style="text-align:center"><sup>K</sup></td>
<td style="text-align:left"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
</tbody>
</table>
<h3 id="emojis" class="tocReference">Emojis</h3>
<p>Emojis are supported, and included into the document using the shortname syntax <code>:shortname:</code>. You can provide more <em>emphasis</em> by using more colons before and after: <code>::shortname::</code>, <code>:::shortname:::</code>, <code>::::shortname::::</code>, etc., each resulting in a larger emoji:</p>
<pre><code class="nohighlight">:smiley:, ::smiley::, :::smiley:::, ::::smiley::::, :::::smiley:::::, etc...
</code></pre>
<p>Result in:</p>
<p><img alt=":smiling face with open mouth:" title="smiley" width="24" height="24" src="/Graphics/Emoji1/svg/1f603.svg"/>, <img alt=":smiling face with open mouth:" title="smiley" width="32" height="32" src="/Graphics/Emoji1/svg/1f603.svg"/>, <img alt=":smiling face with open mouth:" title="smiley" width="48" height="48" src="/Graphics/Emoji1/svg/1f603.svg"/>, <img alt=":smiling face with open mouth:" title="smiley" width="64" height="64" src="/Graphics/Emoji1/svg/1f603.svg"/>, <img alt=":smiling face with open mouth:" title="smiley" width="96" height="96" src="/Graphics/Emoji1/svg/1f603.svg"/>, etc&hellip;</p>
<p>For a list of supported emojis, click <a href="Emojis.md">here</a>.</p>
<h3 id="smileys" class="tocReference">Smileys</h3>
<p>Smileys are supported in markdown text, and converted to the corresponding emojis. For a list of supported smileys, click <a href="Smileys.md">here</a>.</p>
<h3 id="htmlEntities" class="tocReference">HTML Entities</h3>
<p>HTML Entities are supported in markdown text, and converted to the corresponding UNICODE characters. For a list of  supported HTML entities, click <a href="Entities.md">here</a>.</p>
</section>
<section>
<h2 id="blockConstructs" class="tocReference">Block constructs</h2>
<p>Block constructs are larger constructs representing larger blocks in the document. They are all separated from each other using empty rows  (or rows including only white space characters). The following subsections lists the different block constructs that are available in the  <strong>TAG Neuron</strong> version of markdown.</p>
<h3 id="paragraphs" class="tocReference">Paragraphs</h3>
<p>Paragraphs are created by writing blocks of text and separating them with empty rows (or rows with only white space characters). They are placed within <code>&lt;p&gt;</code> and <code>&lt;/p&gt;</code> in the generated HTML. Line breaks in your markdown text files are ignored by the markdown parser and interpreted as normal white space. The generated output will display all text in the paragraph as a continuous block of text, that will adapt itself to the width of the available display area.</p>
<h3 id="lineBreaks" class="tocReference">Line breaks</h3>
<p>If you want to include hard line breaks<br/>
in a paragraph, you must terminate the<br/>
rows you want to break with two space<br/>
characters.</p>
<h3 id="headers" class="tocReference">Headers</h3>
<p>Headers can be written in different ways, depending on what you prefer. A first level header can be written on one row, followed by a row of variable length, containing only equal characters (<code>=</code>), as follows:</p>
<pre><code class="nohighlight">First level header
========================
</code></pre>
<p>A second level header is written in a similar fashion, but instead of equal signs, hyphens (<code>-</code>) are used:</p>
<pre><code class="nohighlight">Second level header
------------------------
</code></pre>
<p>Headers can also be written on a single line, prefixing them with hash signs (<code>#</code>) and a space character. The number of hash signs defines the level of  the header:</p>
<pre><code class="nohighlight"># First level header

## Second level header

### Third level header

#### Fourth level header

...
</code></pre>
<p><strong>Note</strong>: If you omit the space character after the hash signs, you create a <a href="#hashtags">hashtag</a> instead.</p>
<p>If using hash signs to define headers, you can suffix any number of hash signs at the end of the row for clarity in the markown. These will not be displayed in the generated output.</p>
<pre><code class="nohighlight"># First level header #######

## Second level header #####

### Third level header #####

#### Fourth level header ###

...
</code></pre>
<p><strong>Note</strong>: Each header will be assigned a local <em>id</em> that you can link to. You can link to any header in a document, by adding a <em>fragment</em>, starting with the hash sign, and then followed by the automatically generated <em>id</em>. The <em>id</em> is formed by joining the words in the header together using lower case,  capitalizing the first letter of each word except the first word which is kept all lower case. This is called <em>Camel Casing</em>, or <em>camelCasing</em>.  To link to the &ldquo;Block constructs&rdquo; header above, for instance, you would write something like this:</p>
<pre><code class="nohighlight">[Block constructs](#blockConstructs)
</code></pre>
<p>This would result in the following link: <a href="#blockConstructs">Block constructs</a></p>
<p><strong>Note also</strong>: You can easily add a <a href="#tableOfContents">Table of Contents</a> constract to the document. It will automatically generate a table of contents  in the output that will link to all headers available in the document using the automatically generated ids.</p>
<h3 id="blockQuotes" class="tocReference">Block quotes</h3>
<p>Block quotes are blocks of text, where each paragraph is prefixed by a <code>&gt;</code> character and 1-3 space characters (or a tab character). Alternativly, each row in each paragraph of the block quote can be prefixed by the <code>&gt;</code> character and white space, making the text look tidier. Block quotes allow nested constructs.</p>
<p>Example:</p>
<pre><code class="nohighlight">&gt; A block quote can include other block quotes:
&gt; 
&gt; &gt; Like this one
&gt;
&gt; It can include tables:
&gt;
&gt; | a | b |
&gt; |---|---|
&gt; | 1 | 2 |
&gt; | 3 | 4 |
&gt; | 5 | 6 |
&gt;
&gt; Or code:
&gt;
&gt;		10 PRINT "*";
&gt;		20 GOTO 10
&gt;
&gt; It can include lists:
&gt;
&gt;	* Item
&gt;		1. Sub item
&gt;		2. Sub item 2
&gt;	* Item 2
&gt;
&gt; etc.
</code></pre>
<p>This is transformed into:</p>
<blockquote>
<p>A block quote can include other block quotes:</p>
<blockquote>
<p>Like this one</p>
</blockquote>
<p>It can include tables:</p>
<table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:left"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left">a</th>
<th style="text-align:left">b</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">1</td>
<td style="text-align:left">2</td>
</tr>
<tr>
<td style="text-align:left">3</td>
<td style="text-align:left">4</td>
</tr>
<tr>
<td style="text-align:left">5</td>
<td style="text-align:left">6</td>
</tr>
</tbody>
</table>
<p>Or code:</p>
<pre><code class="nohighlight">10 PRINT "*";
	20 GOTO 10
</code></pre>
<p>It can include lists:</p>
<ul>
<li>Item <ol>
<li>Sub item</li>
<li>Sub item 2</li>
</ol>
</li>
<li>Item 2</li>
</ul>
<p>etc.</p>
</blockquote>
<p>The <code>&gt;</code> sign can be optionally prefixed by a <code>+</code> or a <code>-</code> sign to show the block has been inserted (<code>+</code>) or deleted(<code>-</code>). Example:</p>
<pre><code class="nohighlight">+&gt; This paragraph has been added.

This paragraph is unchanged.

-&gt; This paragraph has been deleted.
</code></pre>
<p>This is transformed to:</p>
<blockquote class="inserted">
<p>This paragraph has been added.</p>
</blockquote>
<p>This paragraph is unchanged.</p>
<blockquote class="deleted">
<p>This paragraph has been deleted.</p>
</blockquote>
<h3 id="bulletLists" class="tocReference">Bullet Lists</h3>
<p>Bullet lists are created by simply writing the items prefixed by either asterisks <code>*</code>, plus signs <code>+</code> or minus signs (hyphens) <code>-</code>, followed by one to three space characters or a tab. If the items are written together, as in the following example, Each item will contain just inline text (including inline  constructs):</p>
<pre><code class="nohighlight">* Normal text
* *Emphasized text*
* **Strong text**
</code></pre>
<p>This is displayed as:</p>
<ul>
<li>Normal text</li>
<li><em>Emphasized text</em></li>
<li><strong>Strong text</strong></li>
</ul>
<p>If the items are written with empty rows (or rows including only white space) separating them, the items are formatted as paragraphs:</p>
<pre><code class="nohighlight">+ Normal text

+ *Emphasized text*

+ **Strong text**
</code></pre>
<p>When displayed, this becomes:</p>
<ul>
<li><p>Normal text</p>
</li>
<li><p><em>Emphasized text</em></p>
</li>
<li><p><strong>Strong text</strong></p>
</li>
</ul>
<p>Items can span multiple paragraphs as well. In that case, separate the paragraphs, but make sure to indent at least the first row of each paragraph with 4 space characters, or a tab character. (Each row in the paragraph can be indented, to make the text look tidier, but this is not required.)</p>
<pre><code class="nohighlight">-	This is the first item.

	The first item is written using normal text.

-	*This is the second item.*

	The first item is written using emphasized text.

-	*This is the third item.*

	The third item is written using strong text.
</code></pre>
<p>This results in:</p>
<ul>
<li><p>This is the first item.</p>
<p>The first item is written using normal text.</p>
</li>
<li><p><em>This is the second item.</em></p>
<p>The first item is written using emphasized text.</p>
</li>
<li><p><strong>This is the third item.</strong></p>
<p>The third item is written using strong text.</p>
</li>
</ul>
<h3 id="numberedLists" class="tocReference">Numbered Lists</h3>
<p>Numbered lists are created by simply writing the items prefixed by their corresponding number followed by a period <code>.</code> a space character. The number used will be the number that the item receives in the generated list. As with bullet lists, items written together are treated as inline text, while items separated by empty rows (or rows including only white space) will be treated as items containing paragraphs. Multi-paragraph items are indented. Example of a simple list:</p>
<pre><code class="nohighlight">1. Normal text
10. *Emphasized text*
100. **Strong text**
</code></pre>
<p>This becomes:</p>
<ol>
<li>Normal text</li>
<li value="10"><em>Emphasized text</em></li>
<li value="100"><strong>Strong text</strong></li>
</ol>
<p>An alternative exists to the fixed numbering scheme. Instead of writing the item number, the hash sign (<code>#</code>) can be used to create a lazy numbered list, as follows:</p>
<pre><code class="nohighlight">#. Normal text
#. *Emphasized text*
#. **Strong text**
</code></pre>
<p>This is shown as:</p>
<ol>
<li>Normal text</li>
<li><em>Emphasized text</em></li>
<li><strong>Strong text</strong></li>
</ol>
<p>All types of lists can be nested. The nesting level is kept track of using 4 space characters or 1 tab character per level. Example:</p>
<pre><code class="nohighlight">* Item 1
	#. Item 1.1
		- Item 1.1.1
		- Item 1.1.2
	#. Item 1.2
* Item 2
	#. Item 2.1
		- Item 2.1.1
		- Item 2.1.2
	#. Item 2.2
</code></pre>
<p>This is tranformed to:</p>
<ul>
<li>Item 1 <ol>
<li>Item 1.1 <ul>
<li>Item 1.1.1</li>
<li>Item 1.1.2</li>
</ul>
</li>
<li>Item 1.2</li>
</ol>
</li>
<li>Item 2 <ol>
<li>Item 2.1 <ul>
<li>Item 2.1.1</li>
<li>Item 2.1.2</li>
</ul>
</li>
<li>Item 2.2</li>
</ol>
</li>
</ul>
<h3 id="definitionLists" class="tocReference">Definition Lists</h3>
<p>Definition lists can be used to create glossaries, or similar constructs where terms are defined. A definition list is divided into definition blocks.  Each definition block can have one or more terms followed by a one or more descriptions. The terms are simple inline text, written one term per row.  The descriptions are prefixed by a colon (<code>:</code>) on the first paragraph. If it has more than one paragraph, the first row (at least) each paragraph must  be indented using 1-4 space characters or one tab character. If you want, you can indent all rows in the paragraphs, to make the text easier to read.</p>
<p>A simple definition list only contains a sequence of terms and simple definitions:</p>
<pre><code class="nohighlight">Term 1
:	Definition 1

Term 2
:	Definition 2

Term 3
:	Definition 3
</code></pre>
<p>This becomes:<dt>Term 1</dt>
<dd>Definition 1</dd>
<dt>Term 2</dt>
<dd>Definition 2</dd>
<dt>Term 3</dt>
<dd>Definition 3</dd>
</p>
<p>You can group multiple terms for a definition:</p>
<pre><code class="nohighlight">Term 1
Term 2
:	Definition for Term 1 and 2.

Term 3
:	Definition 3
</code></pre>
<p>Which is transformed to:<dt>Term 1</dt>
<dt>Term 2</dt>
<dd>Definition for Term 1 and 2.</dd>
<dt>Term 3</dt>
<dd>Definition 3</dd>
</p>
<p>You can also have multiple descriptions for a single term:</p>
<pre><code class="nohighlight">Term 1
:	Definition 1.1
:	Definition 1.2

Term 2
:	Definition 2
</code></pre>
<p>This is shown as:<dt>Term 1</dt>
<dd>Definition 1.1</dd>
<dd>Definition 1.2</dd>
<dt>Term 2</dt>
<dd>Definition 2</dd>
</p>
<p>As with the other forms of lists mentioned above, if you include an empty row (or a row with only whitespace) between terms and definitions, definitions are considered paragraphs instead of inline text.</p>
<pre><code class="nohighlight">Term 1

:	Definition 1

Term 2

:	Definition 2

Term 3

:	Definition 3
</code></pre>
<p>Which is displayed as:</p>
<dl>
<dt>Term 1</dt>
<dd><p>Definition 1</p>
</dd>
<dt>Term 2</dt>
<dd><p>Definition 2</p>
</dd>
<dt>Term 3</dt>
<dd><p>Definition 3</p>
</dd>
</dl>
<p>You can also have long descriptions spanning multiple paragraphs, or join types, some of inline type, others of paragraph type.</p>
<pre><code class="nohighlight">Term 1

:	Long Definition for term 1.

	It continues to a second paragraph.

Term 2
:	Definition 2
</code></pre>
<p>Which becomes:</p>
<dl>
<dt>Term 1</dt>
<dd><p>Long Definition for term 1.</p>
<p>It continues to a second paragraph.</p>
</dd>
<dt>Term 2</dt>
<dd>Definition 2</dd>
</dl>
<h3 id="taskLists" class="tocReference">Task lists</h3>
<p>Task lists are lists where items are either checked or unchecked. An unchecked item is prefixed using <code>[ ]</code> (note the single space character). Checked items are prefixed using <code>[x]</code> or <code>[X]</code>. As with bullet lists or numbered lists, items written together are treated as inline text, while items separated by empty rows (or rows including only white space) will be treated as items containing paragraphs. Multi-paragraph items are indented. Example of a simple task list:</p>
<pre><code class="nohighlight">[ ] Unchecked item
[x] Checked item
[X] Another checked item
</code></pre>
<p>This is displayed as:</p>
<ul class="taskList">
<li class="taskListItem"><input disabled="disabled" id="item31373" data-position="31373" type="checkbox"/><span></span><label class="taskListItemLabel" for="item31373">Unchecked item</label></li>
<li class="taskListItem"><input disabled="disabled" id="item31392" data-position="31392" type="checkbox" checked="checked"/><span></span><label class="taskListItemLabel" for="item31392">Checked item</label></li>
<li class="taskListItem"><input disabled="disabled" id="item31409" data-position="31409" type="checkbox" checked="checked"/><span></span><label class="taskListItemLabel" for="item31409">Another checked item</label></li>
</ul>
<p>An example of a nested task list:</p>
<pre><code class="nohighlight">[ ] Unchecked item
[x] Checked item
	[ ] Unchecked subitem
	[x] Checked subitem
	[X] Another checked subitem
[X] A second checked item
</code></pre>
<p>This gets shown as:</p>
<ul class="taskList">
<li class="taskListItem"><input disabled="disabled" id="item31633" data-position="31633" type="checkbox"/><span></span><label class="taskListItemLabel" for="item31633">Unchecked item</label></li>
<li class="taskListItem"><input disabled="disabled" id="item31652" data-position="31652" type="checkbox" checked="checked"/><span></span><label class="taskListItemLabel" for="item31652">Checked item <ul class="taskList">
<li class="taskListItem"><input disabled="disabled" id="item31670" data-position="31670" type="checkbox"/><span></span><label class="taskListItemLabel" for="item31670">Unchecked subitem</label></li>
<li class="taskListItem"><input disabled="disabled" id="item31693" data-position="31693" type="checkbox" checked="checked"/><span></span><label class="taskListItemLabel" for="item31693">Checked subitem</label></li>
<li class="taskListItem"><input disabled="disabled" id="item31714" data-position="31714" type="checkbox" checked="checked"/><span></span><label class="taskListItemLabel" for="item31714">Another checked subitem</label></li>
</ul>
</label></li>
<li class="taskListItem"><input disabled="disabled" id="item31742" data-position="31742" type="checkbox" checked="checked"/><span></span><label class="taskListItemLabel" for="item31742">A second checked item</label></li>
</ul>
<h3 id="horizontalAlignmentOfText" class="tocReference">Horizontal Alignment of text</h3>
<p>You can control horizontal alignment of blocks in Markdown, by using combinations of <code>&lt;&lt;</code> and <code>&gt;&gt;</code> around the contents of the blocks, as illustrated in the following sections. You can choose to put the <code>&lt;&lt;</code> and <code>&gt;&gt;</code> operators on each row, or only on the first or last rows of each block correspondingly.</p>
<p><strong>Note</strong>: For the following examples, you might need to decrease the width of the browser window, to properly see how text alignment works.</p>
<h4 id="leftAlignmentOfText" class="tocReference">Left alignment of text</h4>
<p>Add <code>&lt;&lt;</code> at the beginning of each block, or at the beginning of each row in each block, to left-align the contents. Example:</p>
<pre><code class="nohighlight">&lt;&lt;##### Left-aligned Example
&lt;&lt;
&lt;&lt;This text is left-aligned. Left-alignment is done by placing `&lt;&lt;` in the beginning of each block, or each row in each block,
&lt;&lt;as appropriate.
</code></pre>
<p>This is shown as:</p>
<div class='horizontalAlignLeft'>
<h5 id="leftAlignedExample" class="tocReference">Left-aligned Example</h5>
<p>This text is left-aligned. Left-alignment is done by placing <code>&lt;&lt;</code> in the beginning of each block, or each row in each block, as appropriate.</p>
</div>
<h4 id="rightAlignmentOfText" class="tocReference">Right alignment of text</h4>
<p>Add <code>&gt;&gt;</code> at the end of each block, or at the end of each row in each block, to right-align the contents. Example:</p>
<pre><code class="nohighlight">##### Right-aligned Example&gt;&gt;
&gt;&gt;
This text is right-aligned. Right-alignment is done by placing `&gt;&gt;` at the end of each block, or each row in each block,&gt;&gt;
as appropriate.&gt;&gt;
</code></pre>
<p>This is shown as:</p>
<div class='horizontalAlignRight'>
<h5 id="rightAlignedExample" class="tocReference">Right-aligned Example</h5>
<p>This text is right-aligned. Right-alignment is done by placing <code>&gt;&gt;</code> at the end of each block, or each row in each block, as appropriate.</p>
</div>
<h4 id="centerAlignmentOfText" class="tocReference">Center alignment of text</h4>
<p>Add <code>&gt;&gt;</code> at the beginning of each block, or at the beginning of each row in each block, and <code>&lt;&lt;</code> at the end of each block, or at the end of each row in each block, to center-align the contents. Example:</p>
<pre><code class="nohighlight">&gt;&gt;##### Center-aligned Example&lt;&lt;
&gt;&gt;&lt;&lt;
&gt;&gt;This text is center-aligned. Center-alignment is done by placing `&gt;&gt;` in the beginning of each block, or each row in each block,&lt;&lt;
&gt;&gt;and `&lt;&lt;` at the end of each block, or at the end of each row in each block, as appropriate.&lt;&lt;
</code></pre>
<p>This is shown as:</p>
<div class='horizontalAlignCenter'>
<h5 id="centerAlignedExample" class="tocReference">Center-aligned Example</h5>
<p>This text is center-aligned. Center-alignment is done by placing <code>&gt;&gt;</code> in the beginning of each block, or each row in each block, and <code>&lt;&lt;</code> at the end of each block, or at the end of each row in each block, as appropriate.</p>
</div>
<h4 id="marginAlignmentOfText" class="tocReference">Margin alignment of text</h4>
<p>Add <code>&lt;&lt;</code> at the beginning of each block, or at the beginning of each row in each block, and <code>&gt;&gt;</code> at the end of each block, or at the end of each row in each block, to margin-align the contents. Example:</p>
<pre><code class="nohighlight">&lt;&lt;##### Margin-aligned Example&gt;&gt;
&lt;&lt;&gt;&gt;
&lt;&lt;This text is margin-aligned. Margin-alignment is done by placing `&lt;&lt;` in the beginning of each block, or each row in each block,&gt;&gt;
&lt;&lt;and `&gt;&gt;` at the end of each block, or at the end of each row in each block, as appropriate.&gt;&gt;
</code></pre>
<p>This is shown as:</p>
<div class='horizontalAlignMargins'>
<h5 id="marginAlignedExample" class="tocReference">Margin-aligned Example</h5>
<p>This text is margin-aligned. Margin-alignment is done by placing <code>&lt;&lt;</code> in the beginning of each block, or each row in each block, and <code>&gt;&gt;</code> at the end of each block, or at the end of each row in each block, as appropriate.</p>
</div>
<h3 id="codeBlocks" class="tocReference">Code blocks</h3>
<p>If you want to include larger blocks of code, there are two ways to do this. In both cases you write the code, as-is, with empty rows before and after. You can choose to either indent each line of the code with 1-4 spaces or one tab characters:</p>
<pre><code class="nohighlight">	10 PRINT "*";
	
	20 GOTO 10
</code></pre>
<p>Or, you can write the code without special indentation, but beginning and ending the the block with rows consisting of three or more back ticks  (<code>```</code>), as follows:</p>
<pre><code class="nohighlight">```
10 PRINT "*";

20 GOTO 10
```
</code></pre>
<p>Note that you can insert blank rows in code. Note also that you need to terminate the code block with the same amount of back ticks. The indentation in the first case, or the three (or more) back ticks in the second case, tell the parser when the code block ends. In both cases, you get the following result:</p>
<pre><code class="nohighlight">10 PRINT "*";

20 GOTO 10
</code></pre>
<p>If you want, you can specify the language the code was written in. By doing this, you activate the syntax highlighting feature provided by <a href="https://highlightjs.org/" target="_blank">highlight.js</a>. Example:</p>
<pre><code class="nohighlight">```basic
10 PRINT "*";
20 GOTO 10
```
</code></pre>
<p>This is transformed into:</p>
<pre><code class="basic">10 PRINT "*";
20 GOTO 10
</code></pre>
<p>If the language begins with <code>base64</code>, and the contents is Base64-encoded UTF-8-encoded text, the corresponding text will be decided and displayed, where the language is whatever comes after <code>base64</code>. This method can be used to maintain literal content and syntax, especially  if not aware at design time, and avoid conflicts with the Markdown parser. The following example shows how to present XML from script, in a readable manner, without interfering with the overall structure of the document:</p>
<pre><code class="nohighlight">&#96;&#96;&#96;base64xml
&#123;&#123;Base64Encode(Utf8Encode(PrettyXml(Xml)))&#125;&#125;
&#96;&#96;&#96;</code></pre>
<p><strong>Note</strong>: By default, the <code>default.css</code> highlight style is used on the page, if syntax highlighting using <a href="https://highlightjs.org/" target="_blank">highlight.js</a> is available. The library is accessible through the <code>/Highlight</code> web folder. You can control the style used for highlighting, by including a <code>CSS: /Highlight/style/STYLE_NAME.css</code> header at the top of the page, where <code>STYLE_NAME</code> refers to the actual style to use on the page.</p>
<p><strong>Note 2</strong>: If you use back-ticks, you must use the same amount of back-ticks when closing the code block, as you did when opening the code block.</p>
<p><strong>Note 3</strong>: You can embed code-blocks defined using back-ticks in code-blocks defined by back-ticks, if each embedded code-block uses fewer back-ticks compared to the parent block.</p>
<p>The TAG Neuron provides a pluggable architecture when it comes to rendering code blocks. Depending on the language, the code can be rendered in  different ways. The following subsections illustrate such renderings.</p>
<h4 id="indentationOfHtml" class="tocReference">Indentation of HTML</h4>
<p>It is common to indent HTML code, to make it easier to track nesting of HTML elements on the page. Since HTML can be embedded into Markdown, it is important to be able to allow such HTML code without converting it to code blocks. For this reason, any indented paragraph that starts with a <code>&lt;</code> character will be treated as indented HTML. Instead of rendering it as a code block, the indentation is simply removed, and the contents parsed as normal Markdown. However, if you want to explicitly show HTML in a code block, do not use the indentation method. Instead prefix the HTML with <code>```html</code>, and a <code>```</code> at the end.</p>
<p>Example of indented HTML:</p>
<pre><code class="nohighlight">&lt;div style="background-color: #f0f0f0; border: 1px solid #c0c0c0; padding: 10px; color: black;"&gt;

&lt;p&gt;

This is a paragraph of text, written in *Markdown*.

&lt;/p&gt;

&lt;/div&gt;
</code></pre>
<p>This renders as:</p>
<div style="background-color: #f0f0f0; border: 1px solid #c0c0c0; padding: 10px; color: black;">
<p>This is a paragraph of text, written in <em>Markdown</em>.</p></div>
<h4 id="2dLayoutDiagrams" class="tocReference">2D Layout diagrams</h4>
<p>You can make the Markdown engine transform XML that conforms to the <code>http://waher.se/Schema/Layout2D.xsd</code> namespace directly to images, by placing it in a code block with language <strong>layout</strong>. The layout namespace is defined in the <code>Waher.Layout.Layout2D</code> library. </p>
<p>Example of a <strong>layout</strong> diagram (some parts have been removed for splicity; full example here: <a href="https://github.com/PeterWaher/IoTGateway/blob/master/Layout/Waher.Layout.Layout2D.Test/Xml/Test_39_Stack.xml" target="_blank">GitHub</a>):</p>
<pre><code class="nohighlight">```layout: Neuron architecture
&lt;Layout2D xmlns="http://waher.se/Schema/Layout2D.xsd"
          background="ThemeBackground" font="Text" textColor="Black"&gt;
  &lt;SolidBackground id="ThemeBackground" color="{Theme.BackgroundColor}"/&gt;
  &lt;SolidBackground id="Core" color="{Alpha('Red',128)}"/&gt;
  &lt;SolidBackground id="IoTGateway" color="{Alpha('Orange',128)}"/&gt;
  &lt;SolidBackground id="NeuroLedger" color="{Alpha('Blue',128)}"/&gt;
  &lt;SolidBackground id="Neuron" color="{Alpha('Green',128)}"/&gt;
  &lt;SolidBackground id="App" color="{Alpha('Gray',128)}"/&gt;
  &lt;SolidBackground id="ThirdParty" color="{Alpha('DeepSkyBlue',128)}"/&gt;
  &lt;Font id="Text" name="Arial" size="20pt" color="White"/&gt;
  &lt;Overlays&gt;
    &lt;Grid columns="13"&gt;
      &lt;Cell colSpan="2"/&gt;
      &lt;Cell colSpan="2"&gt;
        &lt;Margins left="1mm" top="1mm" bottom="1mm" right="1mm"&gt;
          &lt;RoundedRectangle radiusX="5mm" radiusY="5mm" height="2cm" fill="ThirdParty"&gt;
            &lt;Margins left="0.5em" right="0.5em"&gt;
			    &lt;Label text="votodirecto.online" x="50%" y="50%" halign="Center"
					    valign="Center" /&gt;
            &lt;/Margins&gt;
          &lt;/RoundedRectangle&gt;
        &lt;/Margins&gt;
      &lt;/Cell&gt;
      &lt;Cell colSpan="2"&gt;
        &lt;Margins left="1mm" top="1mm" bottom="1mm" right="1mm"&gt;
          &lt;RoundedRectangle radiusX="5mm" radiusY="5mm" height="2cm" fill="ThirdParty"&gt;
            &lt;Margins left="0.5em" right="0.5em"&gt;
              &lt;Label text="abc4.io" x="50%" y="50%" halign="Center" valign="Center"/&gt;
            &lt;/Margins&gt;
          &lt;/RoundedRectangle&gt;
        &lt;/Margins&gt;
      &lt;/Cell&gt;
      ...
    &lt;/Grid&gt;
    &lt;Scale scaleX="0.65" scaleY="0.65"&gt;
      &lt;Vertical&gt;
        &lt;Cell&gt;
          &lt;Margins left="1mm" top="1mm" bottom="1mm" right="1mm"&gt;
            &lt;RoundedRectangle radiusX="5mm" radiusY="5mm" fill="ThirdParty"&gt;
              &lt;Margins left="0.5em" right="0.5em" top="0.25em" bottom="0.25em"&gt;
                &lt;Label text="Third Party applications" x="50%" y="50%" halign="Center" valign="Center"/&gt;
              &lt;/Margins&gt;
            &lt;/RoundedRectangle&gt;
          &lt;/Margins&gt;
        &lt;/Cell&gt;
        ...
      &lt;/Vertical&gt;
    &lt;/Scale&gt;
  &lt;/Overlays&gt;
&lt;/Layout2D&gt;
```
</code></pre>
<figure><img src="data:image/png;base64,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5yHVsZCISSlI1oHEFnhlwURvlW08GVlzMqOdHhfq2U7lPdZh3ciKzWqrUlqwEMN6CvAEUvRuDHCVYzGxBQquyG/2IT0bifn2rK2v156fLtioy4N6piDeeu0BgJG6Tf521oTb3daWny/a+ETGxo9lxX2sQ9yHUspdTMRoATqXfrvroTUvze/8O+51hrWOiYiI6C4QGbvp4EXz7xzfICKizdWTza8nvEcmIqL9JNyidIXlQnZERPekON68jpUxrG1ERERERPeOJLk54rkcViy4cs/1ficaML8/bqpvlG3UMBbdLlTBFZmPrP3xvA23eiC0W14smeh7M6YxF1nrKKDXgyo4UHMRzLenTeO7M6YRWtiUhgwFN6rmbuZcxSZvlG1USyyyGnLAgz6YUqtmMV6umqQcN59qTURIRupoO+R7K22uJLAvzpmwksB2u1Cdrkglgf2HeRv+5/dNtbHOft/Je9rxnWkT/umkqb1Xt8ZRgj4PqsOBzEQwfzFp6t+atg2geax8Y9LUrzWQJBbockV6PKgEYl9dsNH/cy2pzEXWagEGgxsVe19ZMNG5qo0i03zPoA9d3KTK8benbeMvJk39emiNu6I9pcjaH86Z8N+PmepEY3sVi9f66nVT/85087cLdPM7ul2o0MK+XrbRTr6j8x48PxARERERERERERERERERERERERHtZ1Kv18cB4M2qcv54WgV73SDaPUMpUb/VJ+kOR+R7M6bxgzl7W6u3Pt8t/nOdyqsksH80YWrtVCTeyXvozvvHRVM/lTabT5O9R7y0oN0XSuLvdTuIiIiINvNgYJPf7k1qG/39P03q1OV6exMIiYjo/vWJnAk/Wdh4tZ///ZrTEbIoIhER7RNpBfu/HIwrG/393Xff9UZGRrw72SYiIrr9RATPPvtseaO/j46OuleuXOHYHhERERHdM5577rlV/d/liqP9rjFczPXeciwlTocjMh/DvF2x90VAk3afABj0uM4NERERERERERERERERERERERER0Z20HPLtdWEGPMsg312uz4fKO5ATGdEfyonrCPBO1SZTIfjb0o4MeNZ0Ozx+iIiIiIiIiIiIiIiIiIiIiIiIiO4kZ+V/fCxnwz+elmCvGkO37oNZcZ8tKE8vlWWej2HfLNtob1tFd7OP5eyGy3YSERERERERERERERHdaYcOHXL7+vrcbDarHMcR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REQ0mVSprtZyKDUIRLdsCfXsWef27s1Xmovedlug9fU62sTsenud5PNuwniqIosXG33ooYQ7enRoUpC2udnoF7+YmBCevXhdjLQO6223BeKmzXyL+frXE7ppU1C+FudEslkn/f3OOScShqo1NWMNzsaI3nyzb3btiuwvf1kx5avLl3vi+6XxhoacGxx0mk6rBIGWm4CjSMyTTyYuvtdT3Re95RZ/pmsBAAAAAAAAcHkI+QIAAAAAAAALlOvoiO3vf18w994biueVApvbtoXx4cNxxbDoDUrr6saqRItFkbNn5+X+6O23+7p9e1gO+MaxuPffL9hnn82Nb+rVDRs888QTCRkNxra0GPPFLybs9743dautaqkxtr/f2Wefzbnf/74U6q2tVWloMKPPW7dvD+TOO8cCvgMDzu7Zk3cvvzwhwKpbtwb6wAORNjSMhUq7u6cOiDc2Gm1uLiVJMxknJ05Maqm1r7ySN21t3miAVZNJkc2bA73ttkCGh507fjx2R47E7qOPirNemwcOFOMDB4oiIt63vlUliYQRKTUJT9X+q9u3h9rWNhY67eqy9umns+7w4Ynzra1V86UvJbS9vdTKG4aiN9/sVwz5el6pxdZacZ98Ettnn83JsWPlMXXLlsA8+mg02mSsTU3G3HVXYPfunXAvzWOPReX76Jy4Y8di++tfTxzrC18Izb33hpJKTVt9q7ff7uuGDWOtwn19zj7zTNa9+25xwoFRJPr44wmzZUup2djzRG+6yZcoylVs8x0Jc9u33y6MD37r6tXeaMBbH3us1OCrWgoD9/RY+6tfZd3Bg2PXMn6NAQAAAAAAAJgXhHwBAAAAAACABcy9+GJO1qzxpLW1VFPb2GjMgw+G9qmnKreyzlZTk/G+/e3qS/5cf7+zP/pRxh06NCkMes0kEmNBw1zOSX///IR877orlGSydK5CQewrr+Tds89OSlO6gwfj+MKFjPnGN5La0lIK+ra2eubznw/sK69M3cQcx+I++KBQDviKiPT1OenrK93nKBK9885Qk8nyz+zPfpZxHR2TnoN7442C9Pdb/cpXklJbq5pMimzZErq33y5cHP7UlSs9SaVKadLeXjvlc+3qsvanP82aJ59M6LJlphy0NUYknVZtb/e1vd2Xxx+PJJt17vRp6z76qOjeeacwPvx8JXTDBr8cbh4cdPb553OTAr4i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" alt="Neuron architecture" title="Neuron architecture" class="aloneUnsized"/><figcaption>Neuron architecture</figcaption></figure>
<p>You can also place a layout graph definition in an <code>.xml</code> file and link to it from an IMG tag in your web pages. It will be automatically converted to an image, as requests from <code>IMG</code> tags request image content only. Example:</p>
<img src="/Images/Layout2DExample.xml"/><p>Results in:</p>
<img src="/Images/Layout2DExample.xml"/>
<p>If you embed the image in a Markdown page, you will need to add an additional image extension to the resource, to let the Markdown parser know you are embedding image content, and not some other form of content. That will explicitly convert the graph to an image of the requested type. The both cases, the graph will be converted to an image of the requested type when requested by the browser. Example:</p>
<pre><code class="nohighlight">![Image Link to 2D Layout diagram](/Images/Layout2DExample.xml.webp)
</code></pre>
<p>Results in:</p>
<figure><img src="/Images/Layout2DExample.xml.webp" alt="Image Link to 2D Layout diagram" class="aloneUnsized"/><figcaption>Image Link to 2D Layout diagram</figcaption></figure>
<p><strong>Note</strong>: Recognized image file extensions are: <code>.webp</code>, <code>.png</code>, <code>.bmp</code>, <code>.gif</code>, <code>.jpg</code>, <code>.jpeg</code>, <code>.tif</code>, <code>.tiff</code>, <code>.wmf</code>, <code>.emf</code> and <code>.ico</code></p>
<h4 id="graphvizDiagrams" class="tocReference">GraphViz diagrams</h4>
<p>If <a href="http://www.graphviz.org/" target="_blank">GraphViz</a> is installed on the same machine as the TAG Neuron, it can be used to render diagrams from code blocks.  There are six diagram types: <strong>dot</strong>, <strong>neato</strong>, <strong>fdp</strong>, <strong>sfdp</strong>, <strong>twopi</strong> and <strong>circo</strong>. Use the corresponding diagram type as language for  the code block. The diagram type can be suffixed by a colon <code>:</code> and a title. The diagram will be rendered as an <em>SVG</em> image.</p>
<p>Example of a <strong>dot</strong> GraphViz diagram:</p>
<pre><code class="nohighlight">```dot: Fancy graph
digraph G { 
	size="4,4"; 
	main [shape=box]; /* this is a comment */ 
	main -&gt; parse [weight=8]; 
	parse -&gt; execute; 
	main -&gt; init [style=dotted]; 
	main -&gt; cleanup; 
	execute -&gt; { make_string; printf} 
	init -&gt; make_string; 
	edge [color=red]; // so is this 
	main -&gt; printf [style=bold,label="100 times"]; 
	make_string [label="make a\nstring"]; 
	node [shape=box,style=filled,color=".7 .3 1.0"]; 
	execute -&gt; compare; 
}
```
</code></pre>
<p>This is rendered as:</p>
<figure><img src="/GraphViz/74c902d0471e47b7ffb8ca7c78a851250919b27435a2a61336ecb43658676771.svg" alt="Fancy graph" title="Fancy graph" class="aloneUnsized"/><figcaption>Fancy graph</figcaption></figure>
<p><strong>Note</strong>: If after having installed <a href="http://www.graphviz.org/" target="_blank">GraphViz</a>, the above is not displayed as a graph, make sure to restart the  TAG Neuron service (or the machine). GraphViz is detected during initialization of the service. Make sure that GraphViz is installed in the  program data folder, preferrably in its default folder.</p>
<p><strong>Note 2</strong>: You can make the graph clickable by embedding <a href="http://www.graphviz.org/doc/info/attrs.html#d:URL" target="_blank">URL attributes</a> on either nodes, edges or the entire graph.</p>
<p><strong>Note 3</strong>: You can use the <a href="GraphVizLab/GraphVizLab.md">GraphViz Lab</a> to experiment with GraphViz syntax.</p>
<p>You can also place a GraphViz graph definition in a <code>.dv</code> or <code>.dot</code> file and link to it from an IMG tag in your web pages. It will be automatically converted to an image, as requests from <code>IMG</code> tags request image content only. Example:</p>
<img src="/Images/GraphVizExample.gv"/><p>Results in:</p>
<img src="/Images/GraphVizExample.gv"/>
<p>If you embed the image in a Markdown page, you will need to add the extension <code>.png</code> or <code>.svg</code> to the resource, to let the Markdown parser know you are embedding image content, and not some other form of content. That will explicitly convert the graph to an image of the requested type (i.e to PNG or SVG formats). The both cases, the graph will be converted to an image of the requested type when requested by the browser. Example:</p>
<pre><code class="nohighlight">![Image Link to GraphViz diagram](/Images/GraphVizExample.gv.png)
</code></pre>
<p>Results in:</p>
<figure><img src="/Images/GraphVizExample.gv.png" alt="Image Link to GraphViz diagram" class="aloneUnsized"/><figcaption>Image Link to GraphViz diagram</figcaption></figure>
<p>For more information about the GraphViz syntax, see the <a href="http://www.graphviz.org/documentation/" target="_blank">GraphViz documentation</a>.</p>
<h4 id="umlWithPlantuml" class="tocReference">UML with PlantUML</h4>
<p>If you have the <a href="http://plantuml.com/download" target="_blank">PlantUML.jar</a> file stored in the program files folder, and have <a href="https://www.java.com" target="_blank">Java</a> installed on the same machine as the TAG Neuron, they can be used to render UML diagrams from code blocks. The diagram will be rendered as an <em>SVG</em> image.</p>
<p>Example of a sequence <strong>uml</strong> PlantUML diagram:</p>
<pre><code class="nohighlight">```uml: Simple Sequence diagram
@startuml
Alice -&gt; Bob: Authentication Request
Bob --&gt; Alice: Authentication Response

Alice -&gt; Bob: Another authentication Request
Alice &lt;-- Bob: another authentication Response
@enduml
```

```uml: Simple Timing diagram
@startuml
robust "Web Browser" as WB
concise "Web User" as WU

@0
WU is Idle
WB is Idle

@100
WU is Waiting
WB is Processing

@300
WB is Waiting
@enduml
```
</code></pre>
<p>This is rendered as:</p>
<figure><img src="/PlantUML/4a189ad8ed9ce0e35e6a68be33fb6b7d86b6933c7db09b1a842aaa24f881358f.svg" alt="Simple Sequence diagram" title="Simple Sequence diagram" class="aloneUnsized"/><figcaption>Simple Sequence diagram</figcaption></figure>
<figure><img src="/PlantUML/a462ad1e9e0fce153ac5cd9bcdb25d1b16bae37ba4e6f887e5e458062c2376dc.svg" alt="Simple Timing diagram" title="Simple Timing diagram" class="aloneUnsized"/><figcaption>Simple Timing diagram</figcaption></figure>
<p><strong>Note</strong>: If after having installed <a href="http://plantuml.com/download" target="_blank">PlantUML</a> and <a href="https://www.java.com" target="_blank">Java</a>, the above is not displayed as a graph,  make sure to restart the TAG Neuron service (or the machine). PlantUML and Java are detected during initialization of the service. Make sure that  PlantUML is installed in the program data folder.</p>
<p><strong>Note 2</strong>: You can use the <a href="PlantUmlLab/PlantUmlLab.md">PlantUML Lab</a> to experiment with PlantUML syntax.</p>
<p>You can also place a PlantUML graph definition in a <code>.uml</code> file and link to it from an IMG tag in your web pages. It will be automatically converted to an image, as requests from <code>IMG</code> tags request image content only. Example:</p>
<img src="/Images/PlantUmlExample.uml"/><p>Results in:</p>
<img src="/Images/PlantUmlExample.uml"/>
<p>If you embed the image in a Markdown page, you will need to add the extension <code>.png</code> or <code>.svg</code> to the resource, to let the Markdown parser know you are embedding image content, and not some other form of content. That will explicitly convert the graph to an image of the requested type (i.e to PNG or SVG formats). The both cases, the graph will be converted to an image of the requested type when requested by the browser. Example:</p>
<pre><code class="nohighlight">![Image Link to PlantUML diagram](/Images/PlantUmlExample.uml.png)
</code></pre>
<p>Results in:</p>
<figure><img src="/Images/PlantUmlExample.uml.png" alt="Image Link to PlantUML diagram" class="aloneUnsized"/><figcaption>Image Link to PlantUML diagram</figcaption></figure>
<p>For more information about PlantUML syntax, see the <a href="http://plantuml.com/PlantUML_Language_Reference_Guide.pdf" target="_blank">PlantUML Language Reference Guide</a>.</p>
<h4 id="embedInlineImages" class="tocReference">Embed inline images</h4>
<p>You can embed an image directly into the Markdown by placing the BASE64-encoded version of the image, together with its image Content-Type, in side a code block.</p>
<p>Example:</p>
<pre><code class="nohighlight">```image/png:PNG as a code block
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAwFBMVEUAAADtTFztTFztTFz5+fkq
X57tTFztTFztTFztTFz5+fkqX57tTFz5+fkqX57tTFztTFztTFztTFz5+fn5+fkqX54qX575+fn5
+fkqX54qX575+fkqX54qX57tTFz5+fn5+fkqX575+fkqX575+fntTFztTFwqX575+fn5+fn5+fkq
X54qX54qX57tTFz5+fkqX56Fosa4yd2ettE3aaTF0+Ls7/NEcqnS3Ojf5u5RfK94mcBehrWSrMxr
j7qrv9fPtihIAAAALnRSTlMA74AQ7+9Aj89gEBCfgIAgv1DfQGBAz4/PYI+fIJ+vIN+/v99QcDBQ
cK8wMK9wikih8QAAA3lJREFUeAHslwVi61AMBD+8MjNjyrQyh3P/U5UhsIZaKncuoMmTtVL+/FKK
X5Yup/f2huQO3OH296dOFt6n9uba1rJ0gS5WNxZ33rb68XpF+kAfuysHb1X9fH1IBsEgbuXMvvrE
2rJQQFldHLctPz0kKSAFNzVuX54BvLkCL08EiILFyFckE2Syqw2HiQvJATmcjqvmfki0AnDlc2Fi
XfJBPislH2FzWWwEsFoqoJeGxEoArsS3uCbFQDEWXz38YiuAV0bCllgLYONt6gvMDXj9RkMtgA1N
/31fL4Cp8t9/CIT5AjazsCSEBuAZCKBAHmwOCSECqhYCLjcTJ2j+JgCQGAhgNW8v8P3jAUBgIYCV
nP0rlCoA1EwEkLmdJ4aEkeCepomAy2rChVAC3NMxEcBpsQn0Wi/UcE/cesEjAvpZrHQ/e4QMokQh
sFswgj2k4mlaAEwV/ALrVVCqddEJuPGiO6gFQku6gdkT0BFs1tBHrW8YYfYE08IIA/QQhGIggCn6
AJwXAxrHsHqCNUnBRxe+hQC/DJaFk6CHxEhgtb/+uRBIGnhGAjjjazhlEQJx/JgBegG+loeyO+CH
oc97gJI4fgfwDsRtuaUdsx6gLAfFOlAD4IePmeCTswQ2PagIp/748+94fIQ6F9DtxE1JIUAQ9gVj
YCSAnSIpFDWlj2ZkJbCY/2eUYyWwQWJQIaALQ/kIAdBjVCGgOE4vP0bghN0iCgHFVbL3MQL7n0dg
6GMEnMUUChT8Cnwagc2PEnj+c3D1Qfx54lfgV+Cm3brAkSSGoQD6HSskRUUHKGGX+N//eCvqcQ/0
QEG89A4QMkXoQnA30cX0+xwg0EXA3Y0ubrhLdJHwgi5gCh0UmEYHDabSQYUZ6WAEzMLuFjzK7C7j
0czuZrwiPqPQZJ8ImI2dbXij+LRBU326kFFhR6J4J/j8RYyKzwOY4PMARsXnAUxweQCHmbjgmcQu
Ep5a2cGK51R8MtDM3f8B6D2WMz6nhZcqii+MwgvJiC8lpwo0tecvoG9LDvimxks0fFtz2t80p/1N
cIq/qS75/ygJTyMJO4yFJykjdtHMU2TFXrPwMJlxgK48aFUckxYesCQcF4Q7ScApNMi+7RVn0SA+
2xuthT9QquJ0WxZ+i+QNF5nzwi8secalxtoKnyitjugi3cI0CV/INIVbwh7//fcL7aUSs7ldhxUA
AAAASUVORK5CYII=
```
</code></pre>
<p>Result:</p>
<figure><img class="aloneUnsized" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAwFBMVEUAAADtTFztTFztTFz5+fkqX57tTFztTFztTFztTFz5+fkqX57tTFz5+fkqX57tTFztTFztTFztTFz5+fn5+fkqX54qX575+fn5+fkqX54qX575+fkqX54qX57tTFz5+fn5+fkqX575+fkqX575+fntTFztTFwqX575+fn5+fn5+fkqX54qX54qX57tTFz5+fkqX56Fosa4yd2ettE3aaTF0+Ls7/NEcqnS3Ojf5u5RfK94mcBehrWSrMxrj7qrv9fPtihIAAAALnRSTlMA74AQ7+9Aj89gEBCfgIAgv1DfQGBAz4/PYI+fIJ+vIN+/v99QcDBQcK8wMK9wikih8QAAA3lJREFUeAHslwVi61AMBD+8MjNjyrQyh3P/U5UhsIZaKncuoMmTtVL+/FKKX5Yup/f2huQO3OH296dOFt6n9uba1rJ0gS5WNxZ33rb68XpF+kAfuysHb1X9fH1IBsEgbuXMvvrE2rJQQFldHLctPz0kKSAFNzVuX54BvLkCL08EiILFyFckE2Syqw2HiQvJATmcjqvmfki0AnDlc2FiXfJBPislH2FzWWwEsFoqoJeGxEoArsS3uCbFQDEWXz38YiuAV0bCllgLYONt6gvMDXj9RkMtgA1N/31fL4Cp8t9/CIT5AjazsCSEBuAZCKBAHmwOCSECqhYCLjcTJ2j+JgCQGAhgNW8v8P3jAUBgIYCVnP0rlCoA1EwEkLmdJ4aEkeCepomAy2rChVAC3NMxEcBpsQn0Wi/UcE/cesEjAvpZrHQ/e4QMokQhsFswgj2k4mlaAEwV/ALrVVCqddEJuPGiO6gFQku6gdkT0BFs1tBHrW8YYfYE08IIA/QQhGIggCn6AJwXAxrHsHqCNUnBRxe+hQC/DJaFk6CHxEhgtb/+uRBIGnhGAjjjazhlEQJx/JgBegG+loeyO+CHoc97gJI4fgfwDsRtuaUdsx6gLAfFOlAD4IePmeCTswQ2PagIp/748+94fIQ6F9DtxE1JIUAQ9gVjYCSAnSIpFDWlj2ZkJbCY/2eUYyWwQWJQIaALQ/kIAdBjVCGgOE4vP0bghN0iCgHFVbL3MQL7n0dg6GMEnMUUChT8Cnwagc2PEnj+c3D1Qfx54lfgV+Cm3brAkSSGoQD6HSskRUUHKGGX+N//eCvqcQ/0QEG89A4QMkXoQnA30cX0+xwg0EXA3Y0ubrhLdJHwgi5gCh0UmEYHDabSQYUZ6WAEzMLuFjzK7C7j0czuZrwiPqPQZJ8ImI2dbXij+LRBU326kFFhR6J4J/j8RYyKzwOY4PMARsXnAUxweQCHmbjgmcQuEp5a2cGK51R8MtDM3f8B6D2WMz6nhZcqii+MwgvJiC8lpwo0tecvoG9LDvimxks0fFtz2t80p/1NcIq/qS75/ygJTyMJO4yFJykjdtHMU2TFXrPwMJlxgK48aFUckxYesCQcF4Q7ScApNMi+7RVn0SA+2xuthT9QquJ0WxZ+i+QNF5nzwi8secalxtoKnyitjugi3cI0CV/INIVbwh7//fcL7aUSs7ldhxUAAAAASUVORK5CYII=" alt="PNG as a code block title="PNG as a code block"/><figcaption>PNG as a code block</figcaption></figure>
<h4 id="embedPdfDocuments" class="tocReference">Embed PDF documents</h4>
<p>You can embed a PDF document directly on the Markdown page using a code block, in a way similar to embedding images. You include the BASE64-encoded contents of the PDF document into the code block, and ensure you use the Internet Content-Type <code>application/pdf</code> for PDF as the language  of the code block.</p>
<p>Example:</p>
<pre><code class="nohighlight">```application/pdf:PDF Document
JVBERi0xLjcNCiW1tbW1DQoxIDAgb2JqDQo8PC9UeXBlL....
....
```
</code></pre>
<p>This will result in an embedded object being rendered in HTML, displaying the contents of the PDF document, if the browser supports embedding documents in HTML 5.</p>
<p>You can also embed PDF documents using the multimedia construct, as shown in the following example:</p>
<pre><code class="nohighlight">![`Harmonized Web API for real-time data.pdf`](https://neuro-foundation.io/Papers/Harmonized%20Web%20API%20for%20real-time%20data.pdf)
</code></pre>
<p>This results in the document being embedded as follows:</p>
<embed type="application/pdf" style="margin-bottom:1em;width:100%;height:75vh;" src="https://neuro-foundation.io/Papers/Harmonized%20Web%20API%20for%20real-time%20data.pdf">

<h3 id="comments" class="tocReference">Comments</h3>
<p>You can add comments to Markdown documents. Comments are not exported when rendering output. Comments are put in separate blocks, each row prefixed by double slash <code>//</code>. Example:</p>
<pre><code class="nohighlight">This is a paragraph

// This is a comment on one row

This is another paragraph

// Comments can be written
// on multiple rows, but
// each row needs to be
// prefixed by //.
</code></pre>
<h3 id="horizontalRules" class="tocReference">Horizontal rules</h3>
<p>Horizontal rules can be used to separate sections of the text. There are various ways of including a horizontal rule. On a separate line, write a line only consisting of asterisks (<code>*</code>) or hyphens (<code>-</code>). You can optionally insert spaces between the asterisks or hyphens if you want. Examples:</p>
<pre><code class="nohighlight">*********************

---------------------

* * * * * * * * * * *

- - - - - - - - - - -
</code></pre>
<p>The all produce the same result:</p>
<hr/>
<hr/>
<hr/>
<hr/>
<h3 id="sections" class="tocReference">Sections</h3>
<p>Sections can be used to divide a longer text into sections, and provide customized layout for each section. Sections are separated using a block consisting of a single row of only equal signs (<code>=</code>). Example:</p>
<pre><code class="nohighlight">===============================
</code></pre>
<p>You can also provide guidance on how many columns you think the new section should have. You can do this by dividing the section separator into blocks, delimited by space characters. The following example creates a section for content that should be displayed in two columns, if column support is provided.</p>
<pre><code class="nohighlight">=============    ==============
</code></pre>
<p>For a section with three columns, write:</p>
<pre><code class="nohighlight">========   =========   ========
</code></pre>
<p>This document is an example of a document that has been divided into sections using section separators.</p>
<p><strong>Note</strong>: Column support is only available in some web clients (HTML). Column support is not available in XAML rendering.</p>
<h3 id="invisibleBreaks" class="tocReference">Invisible breaks</h3>
<p>You can add invisible breaks to your markdown. Such breaks can be used by calling applications to divide the document depending on context. An example can be to cut the document at a logical place to display a brief version of the document. Invisible breaks are inserted using a block consisting of a single row of only tilde signs (<code>~</code>). Example:</p>
<pre><code class="nohighlight">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
</code></pre>
<h3 id="footnotes" class="tocReference">Footnotes</h3>
<p>You can include footnotes into a document in two ways. Either you insert one into the flowing text directly, or by reference. To include a footnote directly into the text you annotate, you include it as follows: <code>[^footnote text]</code>. Note that the foot note text can be formatted using inline constructs. Example:</p>
<pre><code class="nohighlight">In this text we[^With **we**, *we* mean second-person plural] reference a footnote.
</code></pre>
<p>This becomes:</p>
<p>In this text we<sup id="fnref-1"><a href="#fn-1" class="footnote-ref">1</a></sup> reference a footnote.</p>
<p>Note that footnotes in HTML are clickable, and shown at the bottom of the page.</p>
<p>It&rsquo;s also possible to include a footnote through reference. This makes it possible to create a text that is more similar to the final output. However, footnotes are always displayed at the bottom of the page, not the place where you write them in the text. Example:</p>
<pre><code class="nohighlight">In this text we[^we] reference a footnote.
</code></pre>
<p>This is transformed to:</p>
<p>In this text we<sup id="fnref-2"><a href="#fn-2" class="footnote-ref">2</a></sup> reference a footnote.</p>
<p>We also need to write the actual footnote text somewhere in the document. This is done as follows:</p>
<pre><code class="nohighlight">[^we]: With **we**, *we* mean second-person plural
</code></pre>
<p><strong>Note</strong>: The numbers used in footnotes are automatically generated. If you create footnotes such as <code>[^1]: ...</code>, etc., there&rsquo;s no guarantee that the final footnote will actually get the number you used in the text.</p>
<h3 id="tables" class="tocReference">Tables</h3>
<p>Tables are formed by a collection of rows, each row having a given number of cells. A table can also have an optional caption and id. Each column is separated by a pipe character (<code>|</code>). Each row can also optionally start and end with a pipe character. Each row in the table is written using one row in the markdown text. If you want to include a lot of information into the table, consider including content using the <a href="#markdownInclusion">Markdown inclusion</a> operator, described below.</p>
<p>One row in the table is special: It separates the header rows from the content rows of the table. The contents of the columns in this separation row must only be hyphens (<code>-</code>), with optional colons either prefixed or suffixed (or both) to it, to illustrate column alignment. Any white space before and after is ignored. The followig table shows how column alignment is controlled using header separators:</p>
<table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:left"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left">Example</th>
<th style="text-align:left">Meaning</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left"><code>-------</code></td>
<td style="text-align:left">Default alignment</td>
</tr>
<tr>
<td style="text-align:left"><code>:------</code></td>
<td style="text-align:left">Left alignment</td>
</tr>
<tr>
<td style="text-align:left"><code>------:</code></td>
<td style="text-align:left">Right alignment</td>
</tr>
<tr>
<td style="text-align:left"><code>:-----:</code></td>
<td style="text-align:left">Center alignment</td>
</tr>
</tbody>
</table>
<p>Cells can also be joined together horizontally. This is done by leaving the deleted column completely blank, not even including white space.  The preceding column will increase its width in the table, to include the removed cell.</p>
<p>At the end of a table, you can include an optional caption, and an optional id. This is done between brackets. To include only an id, simply add at the end:</p>
<pre><code class="nohighlight">[table_id]
</code></pre>
<p>This id will also be used as a caption for the table. If you want to include a caption that is different from the id, you write:</p>
<pre><code class="nohighlight">[table caption][table_id]
</code></pre>
<p>The following examples, borrowed from <a href="https://rawgit.com/fletcher/human-markdown-reference/master/index.html" target="_blank">MultiMarkdown</a> are illustrative, and show how tables can be built using Markdown:</p>
<pre><code class="nohighlight">| First Header | Second Header |         Third Header |  
| :----------- | :-----------: | -------------------: |  
| First row    |      Data     | Very long data entry |  
| Second row   |    **Cell**   |               *Cell* |  
[simple_table]
</code></pre>
<p>This becomes:</p>
<table>
<caption id="simple_table">simple_table</caption>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left">First Header</th>
<th style="text-align:center">Second Header</th>
<th style="text-align:right">Third Header</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">First row</td>
<td style="text-align:center">Data</td>
<td style="text-align:right">Very long data entry</td>
</tr>
<tr>
<td style="text-align:left">Second row</td>
<td style="text-align:center"><strong>Cell</strong></td>
<td style="text-align:right"><em>Cell</em></td>
</tr>
</tbody>
</table>
<p>A more complex example:</p>
<pre><code class="nohighlight">|              | Grouping                    ||  
| First Header | Second Header | Third Header |  
| ------------ | :-----------: | -----------: |  
| Content      | *Long Cell*                 ||  
| Content      | **Cell**      | Cell         |  
| New section  | More          | Data         |  
[Prototype table][reference_table]
</code></pre>
<p>This is transformed to:</p>
<table>
<caption id="reference_table">Prototype table</caption>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left"></th>
<th style="text-align:center" colspan="2">Grouping</th>
</tr>
<tr>
<th style="text-align:left">First Header</th>
<th style="text-align:center">Second Header</th>
<th style="text-align:right">Third Header</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Content</td>
<td style="text-align:center" colspan="2"><em>Long Cell</em></td>
</tr>
<tr>
<td style="text-align:left">Content</td>
<td style="text-align:center"><strong>Cell</strong></td>
<td style="text-align:right">Cell</td>
</tr>
<tr>
<td style="text-align:left">New section</td>
<td style="text-align:center">More</td>
<td style="text-align:right">Data</td>
</tr>
</tbody>
</table>
<p><strong>Note</strong>: It is not important to keep columns aligned in the markdown text. The Markdown parser makes sure the table is exported correctly. The only reason for maintaining columns in the markdown text aligned, is to make it more readable.</p>
<p>You can provide cell-specific alignment overrides by using the left, right and center alignment constructs within a cell. This can be done both in headers and in data cells of the table. Example:</p>
<pre><code class="nohighlight">| Cell alignment table                        |||
| Left          | Center        | Right         |
| &lt;&lt;Left        | &lt;&lt;Left        | &lt;&lt;Left        |
| Right&gt;&gt;       | Right&gt;&gt;       | Right&gt;&gt;       |
| &gt;&gt;Center&lt;&lt;    | &gt;&gt;Center&lt;&lt;    | &gt;&gt;Center&lt;&lt;    |
|:--------------|:-------------:|--------------:|
| Normal        | Normal        | Normal        |
| &lt;&lt;Left        | &lt;&lt;Left        | &lt;&lt;Left        |
| Right&gt;&gt;       | Right&gt;&gt;       | Right&gt;&gt;       |
| &gt;&gt;Center&lt;&lt;    | &gt;&gt;Center&lt;&lt;    | &gt;&gt;Center&lt;&lt;    |
</code></pre>
<p>This generates a table that looks like:</p>
<table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:center"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="3">Cell alignment table</th>
</tr>
<tr>
<th style="text-align:left">Left</th>
<th style="text-align:center">Center</th>
<th style="text-align:right">Right</th>
</tr>
<tr>
<th style="text-align:left">Left</th>
<th style="text-align:left">Left</th>
<th style="text-align:left">Left</th>
</tr>
<tr>
<th style="text-align:right">Right</th>
<th style="text-align:right">Right</th>
<th style="text-align:right">Right</th>
</tr>
<tr>
<th style="text-align:center">Center</th>
<th style="text-align:center">Center</th>
<th style="text-align:center">Center</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Normal</td>
<td style="text-align:center">Normal</td>
<td style="text-align:right">Normal</td>
</tr>
<tr>
<td style="text-align:left">Left</td>
<td style="text-align:left">Left</td>
<td style="text-align:left">Left</td>
</tr>
<tr>
<td style="text-align:right">Right</td>
<td style="text-align:right">Right</td>
<td style="text-align:right">Right</td>
</tr>
<tr>
<td style="text-align:center">Center</td>
<td style="text-align:center">Center</td>
<td style="text-align:center">Center</td>
</tr>
</tbody>
</table>
<p>You can combine footnotes and tables as a way to create tables with cells that contain more complex content, that does not fit into simple short lines. If a cell has a single footnote reference, it will be assumed that the contents of that footnote should be rendered in the cell, instead of a reference. Example:</p>
<pre><code class="nohighlight">| Table with complex cells ||
|:-------------|:-----------|
| [^e11]       | [^e12]     |
| [^e21]       | [^e22]     |

[^e11]:	| Info about cell ||
    |:--------|-------:|
    | Row     | 1      |
    | Column  | 1      |

[^e12]:	| Info about cell ||
    |:--------|-------:|
    | Row     | 1      |
    | Column  | 2      |

[^e21]:	| Info about cell ||
    |:--------|-------:|
    | Row     | 2      |
    | Column  | 1      |

[^e22]:	| Info about cell ||
    |:--------|-------:|
    | Row     | 2      |
    | Column  | 2      |
</code></pre>
<p>This is rendered as:</p>
<table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:left"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="2">Table with complex cells</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left"><table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="2">Info about cell</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Row</td>
<td style="text-align:right">1</td>
</tr>
<tr>
<td style="text-align:left">Column</td>
<td style="text-align:right">1</td>
</tr>
</tbody>
</table>
</td>
<td style="text-align:left"><table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="2">Info about cell</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Row</td>
<td style="text-align:right">1</td>
</tr>
<tr>
<td style="text-align:left">Column</td>
<td style="text-align:right">2</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr>
<td style="text-align:left"><table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="2">Info about cell</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Row</td>
<td style="text-align:right">2</td>
</tr>
<tr>
<td style="text-align:left">Column</td>
<td style="text-align:right">1</td>
</tr>
</tbody>
</table>
</td>
<td style="text-align:left"><table>
<colgroup>
<col style="text-align:left"/>
<col style="text-align:right"/>
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="2">Info about cell</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Row</td>
<td style="text-align:right">2</td>
</tr>
<tr>
<td style="text-align:left">Column</td>
<td style="text-align:right">2</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<h3 id="blockLevelHtml" class="tocReference">Block-level HTML</h3>
<p>You can add HTML blocks to your markdown text. As with all block constructs, HTML blocks must be separated from other text by empty rows (or rows only including whitespace). The difference between block-level HTML and inline HTML is that block-level HTML reside outside of paragraphs and other similar constructs (i.e. div-type, or block-type HTML constructs are possible), while inline HTML is limited to span-type or inline-type HTML constructs. Block-level HTML can be combined with markdown.</p>
<p>Example:</p>
<div style="border:1px solid black;background-color:#e0e0e0;color:navy;padding:30px;text-align:center">
This text is <u>formatted</u> using <strong>Markdown</strong>.
</div><p>This is shown as:</p>
<div style="border:1px solid black;background-color:#e0e0e0;color:navy;padding:30px;text-align:center">
This text is <u>formatted</u> using <strong>Markdown</strong>.
</div>
</section>
<section>
<h2 id="multimedia" class="tocReference">Multimedia</h2>
<p>Multimedia items are defined in a similar way as links in a markdown document. They can both be defined inline, or by reference, as links are too.  Four things differ, between multimedia links and normal links:</p>
<ol>
<li>The link to a multimedia item must be prefixed by an exclamation mark (<code>!</code>).</li>
<li>The definition can have an optional <code>WIDTH</code> and <code>HEIGHT</code> value after the optional title. Both are positive integers, and both can be provided in both the inline version and the referenced version.</li>
<li>The URL the link is pointing to, selects the best multimedia interface.</li>
<li>It is possible to define multi-resolution or multi-format multimedia content items, by listing a sequence of URLs pointing to resources of different sizes and formats. If the multimedia interface supports multi-format or multi-resolution content, all these resources will be used. If the interface only supports a single source, the first source in the definition will be used. Examples of multi-resolution and multi-format content items will be given below.</li>
</ol>
<p>Developers on the platform can add their own multimedia interfaces. All they need to do is implement a class with a default constructor, that implements the <code>Waher.Content.Markdown.Model.IMultimediaContent</code> interface. The parser will find the class and instantiate it, and then use it for content that it matches. The multimedia interfaces described below only cover the interfaces that are included by default.</p>
<p><strong>Note</strong>: If no particular multimedia handler is found for a URL, it is considered to be an image by default.</p>
<h3 id="images" class="tocReference">Images</h3>
<p>An image can both be included inline, in flowing text, or standalone in a separate block. In the latter case, it&rsquo;s rendered as a figure, with a figure caption. To include an image inline, you can do as follows:</p>
<pre><code class="nohighlight">This is an inline image: ![Smiley](/Graphics/Emoji1/png/64x64/2714.png "Check" 24 24)
</code></pre>
<p>This will be displayed as follows:</p>
<p>This is an inline image: <img src="/Graphics/Emoji1/png/64x64/2714.png" alt="Checkmark" title="Check" width="24" height="24"/></p>
<p>If you put an image on a row by itself, it will be rendered as a figure, with a figure caption. Example:</p>
<pre><code class="nohighlight">![Flag of Chile](/Graphics/Emoji1/png/128x128/1f1e8-1f1f1.png "Check" 128 128)
</code></pre>
<p>This becomes:</p>
<figure><img src="/Graphics/Emoji1/png/128x128/1f1e8-1f1f1.png" alt="Flag of Chile" title="Check" width="128" height="128"/><figcaption>Flag of Chile</figcaption></figure>
<p>You can also define multi-resolution images as follows. In HTML, they are rendered using the <code>&lt;picture&gt;</code> element.</p>
<pre><code class="nohighlight">![Banner](CactusRoseBanner2000x600.png 2000 600)
	(CactusRoseBanner1900x500.png 1900 500)
	(CactusRoseBanner1400x425.png 1400 425)
</code></pre>
<p>Now, the browser will select the most appropriate image, based on available space, if the browser supports responsive images based on the  <code>&lt;picture&gt;</code> element. This is how it will look in your browser:</p>
<figure><picture>
<source srcset="/Themes/CactusRose/CactusRoseBanner2000x600.png" type="image/png" media="(min-width:2000px)"/>
<source srcset="/Themes/CactusRose/CactusRoseBanner1900x500.png" type="image/png" media="(min-width:1900px)"/>
<source srcset="/Themes/CactusRose/CactusRoseBanner1400x425.png" type="image/png" media="(min-width:1400px)"/>
<img src="/Themes/CactusRose/CactusRoseBanner2000x600.png" alt="Banner" srcset="/Themes/CactusRose/CactusRoseBanner2000x600.png 2000w, /Themes/CactusRose/CactusRoseBanner1900x500.png 1900w, /Themes/CactusRose/CactusRoseBanner1400x425.png 1400w" sizes="100vw"/></picture>
<figcaption>Banner</figcaption></figure>
<p>In the same way, you can also define multi-format images using reference notation. You simply list the media items and their different resolutions, if availble one after the other, optionally on separate rows.</p>
<pre><code class="nohighlight">![Cactus Rose][]

[Cactus Rose]: CactusRose1600x1600.png 1600 1600
	CactusRose800x800.png 800 800
</code></pre>
<p>In your browser, this is displayed as:</p>
<figure><picture>
<source srcset="/Themes/CactusRose/CactusRose1600x1600.png" type="image/png" media="(min-width:1600px)"/>
<source srcset="/Themes/CactusRose/CactusRose800x800.png" type="image/png" media="(min-width:800px)"/>
<img src="/Themes/CactusRose/CactusRose1600x1600.png" alt="Cactus Rose" srcset="/Themes/CactusRose/CactusRose1600x1600.png 1600w, /Themes/CactusRose/CactusRose800x800.png 800w" sizes="100vw"/></picture>
<figcaption>Cactus Rose</figcaption></figure>
<p>A short summary:</p>
<ul>
<li><code>&lt;img&gt;</code> elements are used in HTML to display an image.</li>
<li>Multi-resolution images are encapsulated in <code>&lt;picture&gt;</code> elements, where each image is made available in a separate <code>&lt;source&gt;</code> element.</li>
<li>If the image is alone on a paragraph, it is furthermore encapsulated in a <code>&lt;figure&gt;</code> element, and its caption in a <code>&lt;figcapton&gt;</code> element.</li>
</ul>
<h3 id="video" class="tocReference">Video</h3>
<p>You can insert video content into your markdown documents, as you would insert images. The file extension is used to identify the content item as video. When publishing video on web pages, it&rsquo;s important to remember that different clients have support for different video container formats and codecs. For this reason, it&rsquo;s recommended to publish multi-format video so that the client can choose the stream that best suits its capabilities.  Example<sup id="fnref-3"><a href="#fn-3" class="footnote-ref">3</a></sup>:</p>
<pre><code class="nohighlight">![Sample video](/Video/small.webm 560 320)
	(/Video/small.ogv 560 320)
	(/Video/small.mp4 560 320)
	(/Video/small.3gp 352 288)
	(/Video/small.flv 320 240)
</code></pre>
<p>This becomes:</p>
<video controls="controls" width="560" height="320">
<source src="https://waher.se/Video/small.webm" type="video/webm"/>
<source src="https://waher.se/Video/small.ogv" type="video/ogg"/>
<source src="https://waher.se/Video/small.mp4" type="video/mp4"/>
<source src="https://waher.se/Video/small.3gp" type="video/3gpp"/>
<source src="https://waher.se/Video/small.flv" type="video/x-flv"/>
Sample video</video>
<h3 id="audio" class="tocReference">Audio</h3>
<p>You can also insert audio content into your markdown documents. The file extension is used to identify the content item as audio. When publishing audio on web pages, it&rsquo;s important to remember that different clients have support for different audio container formats and codecs. For this reason, it&rsquo;s recommended to publish multi-format audio so that the client can choose the stream that best suits its capabilities. Example<sup id="fnref-4"><a href="#fn-4" class="footnote-ref">4</a></sup>:</p>
<pre><code class="nohighlight">![Sample audio](/Audio/glass_ping-Go445-1207030150.mp3)
	(/Audio/glass_ping-Go445-1207030150.wav)
</code></pre>
<p><strong>Note</strong>: This will not be visible in the browser, but will cause it to play the sound when the page loads, if sound is supported. Audio clips will not loop.</p>
<audio autoplay="autoplay">
<source src="https://waher.se/Audio/glass_ping-Go445-1207030150.mp3" type="audio/mpeg"/>
<source src="https://waher.se/Audio/glass_ping-Go445-1207030150.wav" type="audio/x-wav"/>
Sample audio</audio>
<h3 id="youtube" class="tocReference">YouTube</h3>
<p>To include YouTube clips into your document is easy. A YouTube multimedia content plugin recognizes the YouTube video URL and inserts it accordingly into the generated page inside an <code>&lt;iframe&gt;</code> element. Example:</p>
<pre><code class="nohighlight">![Complex perturbation](https://www.youtube.com/watch?v=whBPLc8m4SU 800 600)
</code></pre>
<p>or:</p>
<pre><code class="nohighlight">![Complex perturbation](https://www.youtu.be/whBPLc8m4SU 800 600)
</code></pre>
<p>This is transformed to:</p>
<iframe src="https://www.youtube.com/embed/whBPLc8m4SU" width="800" height="600">Complex perturbation</iframe>
<h3 id="externalWebPage" class="tocReference">External web page</h3>
<p>You can embed external web content in an <code>&lt;iframe&gt;</code> by using the multimedia inclusion syntax. If the content points to a text page (HTML included), or the resource ends with <code>/</code>, and no other multimedia interface provides a better match, the content is embedded as a web page. Example:</p>
<pre><code class="nohighlight">![Wikipedia](http://wikipedia.com/ 1200 300)
</code></pre>
<p>This becomes:</p>
<iframe src="http://wikipedia.com/" width="1200" height="300">Wikipedia</iframe>
<p><strong>Note</strong>: You can&rsquo;t embed local markdown this way, since it will be included directly into the document, as described <a href="#markdownInclusion">below</a>.</p>
<h3 id="tableOfContents" class="tocReference">Table of Contents</h3>
<p>Inserting a Table of Contents into your document is easy. It&rsquo;s compiled automatically from all headers in the document. To insert it, you simply write the following where you want it inserted. This segment is taken from the Table Of Contents shown at the <a href="#markdownSyntaxReference">top of the page</a>.</p>
<pre><code class="nohighlight">![Table of Contents](ToC)
</code></pre>
<p><strong>Note</strong>: If a page only contains one level 1 header, it&rsquo;s considered a page title, and not included in the table of contents.</p>
<h3 id="markdownInclusion" class="tocReference">Markdown inclusion</h3>
<p>It is possible to include other local markdown documents directly into the flowing text of the current document. This is done by loading the  document, parsing it and generating the corresponding output in the same place where the inclusion was made. This makes it possible to create  reusable markdown templates that you can reuse from your whole site. It also allows you to create output that would not be possible using normal  markdown syntax. You can also pass parameters to the referenced markdown documents using query parameters in the local URL.</p>
<p>Example:</p>
<pre><code class="nohighlight">| Table 3                           | Table     4                       | Table 5                           |
|:---------------------------------:|:---------------------------------:|:---------------------------------:|
|![Table 3](Templates/Repeat.md?x=3)|![Table 4](Templates/Repeat.md?x=4)|![Table 5](Templates/Repeat.md?x=5)|
</code></pre>
<p>Where the contents of the <code>Repeat.md</code> file is:</p>
<pre><code class="nohighlight">| n  | \*{x}  |
|:--:|:------:|
| 1  | {1*x}  |
| 2  | {2*x}  |
| 3  | {3*x}  |
| 4  | {4*x}  |
| 5  | {5*x}  |
| 6  | {6*x}  |
| 7  | {7*x}  |
| 8  | {8*x}  |
| 9  | {9*x}  |
| 10 | {10*x} |
</code></pre>
<p>This is then transformed into:</p>
<table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">Table 3</th>
<th style="text-align:center">Table     4</th>
<th style="text-align:center">Table 5</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">n</th>
<th style="text-align:center">*3</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">1</td>
<td style="text-align:center"><p>3</p>
</td>
</tr>
<tr>
<td style="text-align:center">2</td>
<td style="text-align:center"><p>6</p>
</td>
</tr>
<tr>
<td style="text-align:center">3</td>
<td style="text-align:center"><p>9</p>
</td>
</tr>
<tr>
<td style="text-align:center">4</td>
<td style="text-align:center"><p>12</p>
</td>
</tr>
<tr>
<td style="text-align:center">5</td>
<td style="text-align:center"><p>15</p>
</td>
</tr>
<tr>
<td style="text-align:center">6</td>
<td style="text-align:center"><p>18</p>
</td>
</tr>
<tr>
<td style="text-align:center">7</td>
<td style="text-align:center"><p>21</p>
</td>
</tr>
<tr>
<td style="text-align:center">8</td>
<td style="text-align:center"><p>24</p>
</td>
</tr>
<tr>
<td style="text-align:center">9</td>
<td style="text-align:center"><p>27</p>
</td>
</tr>
<tr>
<td style="text-align:center">10</td>
<td style="text-align:center"><p>30</p>
</td>
</tr>
</tbody>
</table>

</td>
<td style="text-align:center"><table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">n</th>
<th style="text-align:center">*4</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">1</td>
<td style="text-align:center"><p>4</p>
</td>
</tr>
<tr>
<td style="text-align:center">2</td>
<td style="text-align:center"><p>8</p>
</td>
</tr>
<tr>
<td style="text-align:center">3</td>
<td style="text-align:center"><p>12</p>
</td>
</tr>
<tr>
<td style="text-align:center">4</td>
<td style="text-align:center"><p>16</p>
</td>
</tr>
<tr>
<td style="text-align:center">5</td>
<td style="text-align:center"><p>20</p>
</td>
</tr>
<tr>
<td style="text-align:center">6</td>
<td style="text-align:center"><p>24</p>
</td>
</tr>
<tr>
<td style="text-align:center">7</td>
<td style="text-align:center"><p>28</p>
</td>
</tr>
<tr>
<td style="text-align:center">8</td>
<td style="text-align:center"><p>32</p>
</td>
</tr>
<tr>
<td style="text-align:center">9</td>
<td style="text-align:center"><p>36</p>
</td>
</tr>
<tr>
<td style="text-align:center">10</td>
<td style="text-align:center"><p>40</p>
</td>
</tr>
</tbody>
</table>

</td>
<td style="text-align:center"><table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">n</th>
<th style="text-align:center">*5</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">1</td>
<td style="text-align:center"><p>5</p>
</td>
</tr>
<tr>
<td style="text-align:center">2</td>
<td style="text-align:center"><p>10</p>
</td>
</tr>
<tr>
<td style="text-align:center">3</td>
<td style="text-align:center"><p>15</p>
</td>
</tr>
<tr>
<td style="text-align:center">4</td>
<td style="text-align:center"><p>20</p>
</td>
</tr>
<tr>
<td style="text-align:center">5</td>
<td style="text-align:center"><p>25</p>
</td>
</tr>
<tr>
<td style="text-align:center">6</td>
<td style="text-align:center"><p>30</p>
</td>
</tr>
<tr>
<td style="text-align:center">7</td>
<td style="text-align:center"><p>35</p>
</td>
</tr>
<tr>
<td style="text-align:center">8</td>
<td style="text-align:center"><p>40</p>
</td>
</tr>
<tr>
<td style="text-align:center">9</td>
<td style="text-align:center"><p>45</p>
</td>
</tr>
<tr>
<td style="text-align:center">10</td>
<td style="text-align:center"><p>50</p>
</td>
</tr>
</tbody>
</table>

</td>
</tr>
</tbody>
</table>
<p><strong>Note</strong>: Remember that the inclusion paths of the markdown content you want to include, are relative to the location of the main markdown file. The system will detect circular references and return an error if you try to create a document that creates such a circular reference. Also,  included markdown files must not contain any metadata.</p>
<p><strong>Note 2</strong>: Script parameters can be either <strong>double</strong>, <strong>boolean</strong> or <strong>string</strong> values. If the value cannot be parsed as a double or a boolean value, it is taken to be a string. Any further parsing must be done by script in the template.</p>
</section>
<section>
<h2 id="script" class="tocReference">Script</h2>
<p><a href="Script.md">Script</a> can be used to make your markdown pages dynamic. The following sections describe different options. For more information about script, see the <a href="Script.md">Script reference</a>. You can also use the <a href="Prompt.md">Prompt</a> to experiment with script syntax.</p>
<p>Script in Markdown can be processed in three different ways:</p>
<ol>
<li><strong>Inline processing</strong>: The script is evaluated as part of rendering, and the result presented in the place of the script.</li>
<li><strong>Pre-processing</strong>: Script is evaluated prior to rendering the page for display. This allows script to modify the structure of the Markdown document.</li>
<li><strong>Asynchronous processing</strong>: Long-running script can be run asynchronously. This means the page is rendered and returned to the client. When the script is evaluated, it is returned to the client, which inserts it in the place of the script.</li>
</ol>
<h3 id="inlineScript" class="tocReference">Inline script</h3>
<p><a href="Script.md">Script</a> can be embedded inline in a block, between curly braces <code>{</code> and <code>}</code>. The result is then presented in the final output. Example:</p>
<pre><code class="nohighlight">*a* is {a:=5} and *b* is {b:=6}. *a*\**b* is therefore {a*b}.
</code></pre>
<p>This becomes:</p>
<p><em>a</em> is 5 and <em>b</em> is 6. <em>a</em>*<em>b</em> is therefore 30.</p>
<p><strong>Note</strong>: Inline script must all reside in a block. While new-line can be used in such inline script, empty rows separating blocks cannot.</p>
<h4 id="graphs" class="tocReference">Graphs</h4>
<p>If you use inline script, the result may control how the data is output. Normally, strings are inserted. But graphs and images can also be generated in script. In these cases, they are displayed directly. Example:</p>
<pre><code class="nohighlight">{
GraphWidth:=800;
GraphHeight:=400;
x:=-10..10|0.1;
y:=sin(5*x)*exp(-(x^2/10));
plot2dcurve(x,y)
}
</code></pre>
<p>This script is evaluated as:</p>
<figure><img border="2" width="800" height="400" src="data:image/png;base64,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" alt="Graph" /></figure>
<h3 id="preProcessedScript" class="tocReference">Pre-processed script</h3>
<p>Pre-processed script is inserted into the markdown page between double curly braces <code>{{</code> and <code>}}</code>. Such script is  evaluated before parsing the markdown, and the script is replaced by the result, <em>as strings</em>. Normal inline script between single braces are  evaluated after markdown processing, and can contain any type of result. Such script does not change the structure of the markdown document.  Pre-processed script however, can change the actual structure and formatting of the document.</p>
<p>Example:</p>
<pre><code class="nohighlight">
Result of execution: &#123;&#123;s:=&quot;some text&quot;;&quot;**&quot;+s+&quot;**&quot;&#125;&#125;.
</code></pre>
<p>This is transformed to:</p>
<p>Result of execution: <strong>some text</strong>.</p>
<h4 id="loopsAndDynamicContent" class="tocReference">Loops and dynamic content</h4>
<p>You can use the <em>implicit print</em> operation in script to dynamically fill the document with contents available though script. This makes it possible to create dynamic documents with markdown, and not only static ones. The basics consists of defining the script as a pre-processed script block, and implicitly printing the contents. The following example illustrates this point, by creating a multiplication table:</p>
<p><pre><code class="nohighlight">
| \* |{{
for each x in 1..15 do
	]] ((x)) |[[;
&nbsp;<br/>
]]
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|[[;
&nbsp;<br/>
for each y in 1..15 do
(
	]]
| **((y))** |[[;
&nbsp;<br/>
	for each x in 1..15 do
		]] ((x<em>y)) |[[;
)
}}
</code></pre></em></p>
<table>
<colgroup>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
<col style="text-align:center"/>
</colgroup>
<thead>
<tr>
<th style="text-align:center">*</th>
<th style="text-align:center">1</th>
<th style="text-align:center">2</th>
<th style="text-align:center">3</th>
<th style="text-align:center">4</th>
<th style="text-align:center">5</th>
<th style="text-align:center">6</th>
<th style="text-align:center">7</th>
<th style="text-align:center">8</th>
<th style="text-align:center">9</th>
<th style="text-align:center">10</th>
<th style="text-align:center">11</th>
<th style="text-align:center">12</th>
<th style="text-align:center">13</th>
<th style="text-align:center">14</th>
<th style="text-align:center">15</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><strong>1</strong></td>
<td style="text-align:center">1</td>
<td style="text-align:center">2</td>
<td style="text-align:center">3</td>
<td style="text-align:center">4</td>
<td style="text-align:center">5</td>
<td style="text-align:center">6</td>
<td style="text-align:center">7</td>
<td style="text-align:center">8</td>
<td style="text-align:center">9</td>
<td style="text-align:center">10</td>
<td style="text-align:center">11</td>
<td style="text-align:center">12</td>
<td style="text-align:center">13</td>
<td style="text-align:center">14</td>
<td style="text-align:center">15</td>
</tr>
<tr>
<td style="text-align:center"><strong>2</strong></td>
<td style="text-align:center">2</td>
<td style="text-align:center">4</td>
<td style="text-align:center">6</td>
<td style="text-align:center">8</td>
<td style="text-align:center">10</td>
<td style="text-align:center">12</td>
<td style="text-align:center">14</td>
<td style="text-align:center">16</td>
<td style="text-align:center">18</td>
<td style="text-align:center">20</td>
<td style="text-align:center">22</td>
<td style="text-align:center">24</td>
<td style="text-align:center">26</td>
<td style="text-align:center">28</td>
<td style="text-align:center">30</td>
</tr>
<tr>
<td style="text-align:center"><strong>3</strong></td>
<td style="text-align:center">3</td>
<td style="text-align:center">6</td>
<td style="text-align:center">9</td>
<td style="text-align:center">12</td>
<td style="text-align:center">15</td>
<td style="text-align:center">18</td>
<td style="text-align:center">21</td>
<td style="text-align:center">24</td>
<td style="text-align:center">27</td>
<td style="text-align:center">30</td>
<td style="text-align:center">33</td>
<td style="text-align:center">36</td>
<td style="text-align:center">39</td>
<td style="text-align:center">42</td>
<td style="text-align:center">45</td>
</tr>
<tr>
<td style="text-align:center"><strong>4</strong></td>
<td style="text-align:center">4</td>
<td style="text-align:center">8</td>
<td style="text-align:center">12</td>
<td style="text-align:center">16</td>
<td style="text-align:center">20</td>
<td style="text-align:center">24</td>
<td style="text-align:center">28</td>
<td style="text-align:center">32</td>
<td style="text-align:center">36</td>
<td style="text-align:center">40</td>
<td style="text-align:center">44</td>
<td style="text-align:center">48</td>
<td style="text-align:center">52</td>
<td style="text-align:center">56</td>
<td style="text-align:center">60</td>
</tr>
<tr>
<td style="text-align:center"><strong>5</strong></td>
<td style="text-align:center">5</td>
<td style="text-align:center">10</td>
<td style="text-align:center">15</td>
<td style="text-align:center">20</td>
<td style="text-align:center">25</td>
<td style="text-align:center">30</td>
<td style="text-align:center">35</td>
<td style="text-align:center">40</td>
<td style="text-align:center">45</td>
<td style="text-align:center">50</td>
<td style="text-align:center">55</td>
<td style="text-align:center">60</td>
<td style="text-align:center">65</td>
<td style="text-align:center">70</td>
<td style="text-align:center">75</td>
</tr>
<tr>
<td style="text-align:center"><strong>6</strong></td>
<td style="text-align:center">6</td>
<td style="text-align:center">12</td>
<td style="text-align:center">18</td>
<td style="text-align:center">24</td>
<td style="text-align:center">30</td>
<td style="text-align:center">36</td>
<td style="text-align:center">42</td>
<td style="text-align:center">48</td>
<td style="text-align:center">54</td>
<td style="text-align:center">60</td>
<td style="text-align:center">66</td>
<td style="text-align:center">72</td>
<td style="text-align:center">78</td>
<td style="text-align:center">84</td>
<td style="text-align:center">90</td>
</tr>
<tr>
<td style="text-align:center"><strong>7</strong></td>
<td style="text-align:center">7</td>
<td style="text-align:center">14</td>
<td style="text-align:center">21</td>
<td style="text-align:center">28</td>
<td style="text-align:center">35</td>
<td style="text-align:center">42</td>
<td style="text-align:center">49</td>
<td style="text-align:center">56</td>
<td style="text-align:center">63</td>
<td style="text-align:center">70</td>
<td style="text-align:center">77</td>
<td style="text-align:center">84</td>
<td style="text-align:center">91</td>
<td style="text-align:center">98</td>
<td style="text-align:center">105</td>
</tr>
<tr>
<td style="text-align:center"><strong>8</strong></td>
<td style="text-align:center">8</td>
<td style="text-align:center">16</td>
<td style="text-align:center">24</td>
<td style="text-align:center">32</td>
<td style="text-align:center">40</td>
<td style="text-align:center">48</td>
<td style="text-align:center">56</td>
<td style="text-align:center">64</td>
<td style="text-align:center">72</td>
<td style="text-align:center">80</td>
<td style="text-align:center">88</td>
<td style="text-align:center">96</td>
<td style="text-align:center">104</td>
<td style="text-align:center">112</td>
<td style="text-align:center">120</td>
</tr>
<tr>
<td style="text-align:center"><strong>9</strong></td>
<td style="text-align:center">9</td>
<td style="text-align:center">18</td>
<td style="text-align:center">27</td>
<td style="text-align:center">36</td>
<td style="text-align:center">45</td>
<td style="text-align:center">54</td>
<td style="text-align:center">63</td>
<td style="text-align:center">72</td>
<td style="text-align:center">81</td>
<td style="text-align:center">90</td>
<td style="text-align:center">99</td>
<td style="text-align:center">108</td>
<td style="text-align:center">117</td>
<td style="text-align:center">126</td>
<td style="text-align:center">135</td>
</tr>
<tr>
<td style="text-align:center"><strong>10</strong></td>
<td style="text-align:center">10</td>
<td style="text-align:center">20</td>
<td style="text-align:center">30</td>
<td style="text-align:center">40</td>
<td style="text-align:center">50</td>
<td style="text-align:center">60</td>
<td style="text-align:center">70</td>
<td style="text-align:center">80</td>
<td style="text-align:center">90</td>
<td style="text-align:center">100</td>
<td style="text-align:center">110</td>
<td style="text-align:center">120</td>
<td style="text-align:center">130</td>
<td style="text-align:center">140</td>
<td style="text-align:center">150</td>
</tr>
<tr>
<td style="text-align:center"><strong>11</strong></td>
<td style="text-align:center">11</td>
<td style="text-align:center">22</td>
<td style="text-align:center">33</td>
<td style="text-align:center">44</td>
<td style="text-align:center">55</td>
<td style="text-align:center">66</td>
<td style="text-align:center">77</td>
<td style="text-align:center">88</td>
<td style="text-align:center">99</td>
<td style="text-align:center">110</td>
<td style="text-align:center">121</td>
<td style="text-align:center">132</td>
<td style="text-align:center">143</td>
<td style="text-align:center">154</td>
<td style="text-align:center">165</td>
</tr>
<tr>
<td style="text-align:center"><strong>12</strong></td>
<td style="text-align:center">12</td>
<td style="text-align:center">24</td>
<td style="text-align:center">36</td>
<td style="text-align:center">48</td>
<td style="text-align:center">60</td>
<td style="text-align:center">72</td>
<td style="text-align:center">84</td>
<td style="text-align:center">96</td>
<td style="text-align:center">108</td>
<td style="text-align:center">120</td>
<td style="text-align:center">132</td>
<td style="text-align:center">144</td>
<td style="text-align:center">156</td>
<td style="text-align:center">168</td>
<td style="text-align:center">180</td>
</tr>
<tr>
<td style="text-align:center"><strong>13</strong></td>
<td style="text-align:center">13</td>
<td style="text-align:center">26</td>
<td style="text-align:center">39</td>
<td style="text-align:center">52</td>
<td style="text-align:center">65</td>
<td style="text-align:center">78</td>
<td style="text-align:center">91</td>
<td style="text-align:center">104</td>
<td style="text-align:center">117</td>
<td style="text-align:center">130</td>
<td style="text-align:center">143</td>
<td style="text-align:center">156</td>
<td style="text-align:center">169</td>
<td style="text-align:center">182</td>
<td style="text-align:center">195</td>
</tr>
<tr>
<td style="text-align:center"><strong>14</strong></td>
<td style="text-align:center">14</td>
<td style="text-align:center">28</td>
<td style="text-align:center">42</td>
<td style="text-align:center">56</td>
<td style="text-align:center">70</td>
<td style="text-align:center">84</td>
<td style="text-align:center">98</td>
<td style="text-align:center">112</td>
<td style="text-align:center">126</td>
<td style="text-align:center">140</td>
<td style="text-align:center">154</td>
<td style="text-align:center">168</td>
<td style="text-align:center">182</td>
<td style="text-align:center">196</td>
<td style="text-align:center">210</td>
</tr>
<tr>
<td style="text-align:center"><strong>15</strong></td>
<td style="text-align:center">15</td>
<td style="text-align:center">30</td>
<td style="text-align:center">45</td>
<td style="text-align:center">60</td>
<td style="text-align:center">75</td>
<td style="text-align:center">90</td>
<td style="text-align:center">105</td>
<td style="text-align:center">120</td>
<td style="text-align:center">135</td>
<td style="text-align:center">150</td>
<td style="text-align:center">165</td>
<td style="text-align:center">180</td>
<td style="text-align:center">195</td>
<td style="text-align:center">210</td>
<td style="text-align:center">225</td>
</tr>
</tbody>
</table>
<h3 id="asynchronousProcessingOfScript" class="tocReference">Asynchronous processing of script</h3>
<p>It is possible to execute script on the page asynchronously as well. This is done by adding a <em>Code Block</em> of type <code>async</code>. The <code>async</code> can be succeeded by a colon (<code>:</code>) and some text that will be displayed while the script is being executed and the result loaded to the client. You can use the <code>preview</code> function to display a partial result during the calculation. Example:</p>
<pre><code class="nohighlight">```async:Previewing intermediate results
PlotCPU(TP[],CPU[]):=
(
    one:=Ones(count(TP));
    TP2:=TP.^2;
    TP3:=TP.^3;
    M1:=[one,TP];
    M2:=[one,TP,TP2];
    M3:=[one,TP,TP2,TP3];
    [[a1,b1]]:=((CPU[,])*(M1 T))*inv(M1*(M1 T));
    [[a2,b2,c2]]:=((CPU[,])*(M2 T))*inv(M2*(M2 T));
    [[a3,b3,c3,d3]]:=((CPU[,])*(M3 T))*inv(M3*(M3 T));
    G:=plot2dcurve(TP,avg(CPU)*one,"Blue")+
        plot2dcurve(TP,a1+b1*TP,"Green")+
        plot2dcurve(TP,a2+b2*TP+c2*TP2,"Yellow")+
        plot2dcurve(TP,a3+b3*TP+c3*TP2+d3*TP3,"Orange")+
        plot2dcurve(TP,CPU,"Red",5);
    G.Title:="CPU";
    G.LabelX:="Time (s)";
    G.LabelY:="CPU (%)";
    G
);

TP:=[];
CPU:=[];
Start:=Now;
foreach x in 1..60 do
(
    Sleep(1000);
    CPU:=join(CPU,(PerformanceCounterValue("Processor","_Total","% Processor Time") ??? Uniform(0,100)));
    TP:=join(TP,Now.Subtract(Start).TotalSeconds);
    preview(PlotCPU(TP,CPU))
);
```
</code></pre>
<p>This generates the following result (reload to restart):</p>
<div id="id44d9d6ab11cc6be9c232168cb17616088a1b55ee72d1637cb7c4ef45ff519f6a">Previewing intermediate results</div>
<script type="text/javascript">LoadContent("44d9d6ab11cc6be9c232168cb17616088a1b55ee72d1637cb7c4ef45ff519f6a");</script>
<p><strong>Note</strong>: If the script returns XML, and there is an XML Visualizer available in the code (i.e.a class that has implemented <code>Waher.Content.Markdown.Model.XmlVisualizer</code>), the XML is first transformed before being visualized. For example, script may compute a 2D Layout XML document, that is then used to generate a visual image, as shown in the following example:</p>
<pre><code class="nohighlight">```async:Some statistics
&lt;Layout2D xmlns="http://waher.se/Schema/Layout2D.xsd"
          background="ThemeBackground" pen="BlackPen"
          font="Text" textColor="Black"&gt;
    &lt;SolidPen id="BlackPen" color="Black" width="1px"/&gt;
    &lt;SolidPen id="LightGrayPen" color="LightGray" width="1px"/&gt;
    &lt;SolidPen id="GreenPen" color="Green" width="2mm"/&gt;
    &lt;SolidPen id="RedPen" color="Red" width="2mm"/&gt;
    &lt;SolidBackground id="ThemeBackground" color="{Theme.BackgroundColor}"/&gt;
    &lt;SolidBackground id="GreenBackground" color="{Alpha('Green',128)}"/&gt;
    &lt;SolidBackground id="RedBackground" color="{Alpha('Red',128)}"/&gt;
    &lt;Font id="Text" name="Arial" size="36pt" color="White"/&gt;
    &lt;Rectangle x="0%" y="0%" x2="100%" y2="100%" pen="BlackPen" fill="ThemeBackground"/&gt;
    &lt;ForEach variable="k" expression="(10..90|10)+'%'"&gt;
	    &lt;Line x="{k}" y="0%" x2="{k}" y2="100%" pen="LightGrayPen"/&gt;
	    &lt;Line x="0%" y="{k}" x2="100%" y2="{k}" pen="LightGrayPen"/&gt;
    &lt;/ForEach&gt;
    &lt;CircleArc x="45%" y="50%" radius="30%" startDegrees="{Ok:=20;Total:=24;DegGreen:=360*Ok/Total;DegRed:=360-DegGreen;DegRed/2}" endDegrees="{360-DegRed/2}" clockwise="true" center="true" pen="GreenPen" fill="GreenBackground"/&gt;
    &lt;CircleArc x="55%" y="50%" radius="30%" startDegrees="{360-DegRed/2}" endDegrees="{DegRed/2}" clockwise="true" center="true" pen="RedPen" fill="RedBackground"/&gt;
    &lt;Label x="30%" y="50%" font="Text" halign="Center" valign="Center" text="{Ok}"/&gt;
    &lt;Label x="70%" y="50%" font="Text" halign="Center" valign="Center" text="{Total-Ok}"/&gt;
&lt;/Layout2D&gt;
```
</code></pre>
<p>Is shown as</p>
<div id="id2017b69c4de6459a0575647ac1c3d202eb6b606835362de36dd9e8507dc789e6">Some statistics</div>
<script type="text/javascript">LoadContent("2017b69c4de6459a0575647ac1c3d202eb6b606835362de36dd9e8507dc789e6");</script>
<h3 id="sessionsAndVariables" class="tocReference">Sessions and variables</h3>
<p>When a user connects to the server, it will receive a session. This session will maintain all variables that is created in script. These variabes will be available from any page the user views. Each user will have its own set of variables stored in its own session. If the user does not access the server for 20 minutes by default, the session is lost, and any variables created will be lost.</p>
<h3 id="queryParameters" class="tocReference">Query parameters</h3>
<p>When loading a markdown page, any query parameters listed using the <a href="#parameter">PARAMETER metadata tag</a> will be available as variables in script.  If the query variable is not available, the parameter will be set to the empty string. By default, the variable type is a string, unless it can be parsed as a double number or a boolean value.</p>
<h3 id="globalVariables" class="tocReference">Global variables</h3>
<p>When a user session is created, it will contain a variable named <code>Global</code> that points to a global variables collection. The global variables collection and the session variables collection can be used by resources to keep application states. States will be available  for all script on the server, if accessed through the <code>Global</code> variables collection.</p>
<p>Example:</p>
<pre><code class="nohighlight">This page has been viewed {Global.NrTimesMarkdownLoaded:=exists(Global.NrTimesMarkdownLoaded) ? Global.NrTimesMarkdownLoaded+1 : 1} times since the server was last restarted.
</code></pre>
<p>This becomes:</p>
<p>This page has been viewed 579 times since the server was last restarted.</p>
<p><strong>Note</strong>: If the count does not increment when the page is loaded or refreshed, it means you&rsquo;re receiving a cached result. You can control page cache rules using <a href="#metadata">Metadata tags</a>.</p>
<h3 id="pageLocalVariables" class="tocReference">Page-local variables</h3>
<p>When navigating on Markdown pages, a page-local collection of variables is available, by referencing the session variable named <code>Page</code>.  Every time a new page is viewed by the same session, the Page-collection is cleared. The <code>Page</code> collection can be a good place to store temporary information related to the current page.</p>
<p>Example:</p>
<pre><code class="nohighlight">This page has been viewed {Page.NrTimesMarkdownLoaded:=exists(Page.NrTimesMarkdownLoaded) ? Page.NrTimesMarkdownLoaded+1 : 1} times since you last navigated to this page.
</code></pre>
<p>This becomes:</p>
<p>This page has been viewed 1 times since you last navigated to this page.</p>
<h3 id="currentRequest" class="tocReference">Current request</h3>
<p>The session state will contain a variable named <code>Request</code> that contains detailed information about the current request. The variable will contain an object of type <code>Waher.Networking.HTTP.HttpRequest</code>.</p>
<h3 id="currentResponse" class="tocReference">Current response</h3>
<p>The session state will contain a variable named <code>Response</code> where the response is being built. The variable will contain an object of type  <code>Waher.Networking.HTTP.HttpResponse</code>. It can be used to set custom header information, etc.</p>
<h3 id="postedData" class="tocReference">Posted data</h3>
<p>Data posted to a page can be accessed, in decoded form, by accessing the <code>Posted</code> variable, defined in the <code>Waher.Networking.HTTP</code> module. This makes it possible to implement a form into a Markdown page, and process posted information from script embedded in the document itself, or linked to it in the meta-data headers.</p>
<h3 id="webServices" class="tocReference">Web Services</h3>
<p>There are multiple ways to define web services using Markdown and/or script, as outlined in the following sub-sections.</p>
<h4 id="webScript" class="tocReference">Web Script</h4>
<p>Web Script (Web Service, or <em>Waher Script</em>) is script that is stored in files with extension <code>.ws</code>. A client can POST data to such a Web Script file. The data will be decoded and made available in the script through the <code>Posted</code> variable. The result of the script is then encoded to the client, based on the <code>Accept</code> header in the HTTP Request. For JSON responses, the <code>Accept</code> header should have the value <code>application/json</code>.</p>
<h4 id="markdownBasedServices" class="tocReference">Markdown-based Services</h4>
<p>You can create separate Markdown files with the <a href="#bodyOnly"><code>BodyOnly</code></a> meta-data tag set to <code>true</code>, to create web services that return HTML directly. This is suitable if the response does not need to be parsed and conditionally processed, but only displayed to the user. A client POSTs data to such a Markdown file. The data will be decoded and made available in the script through the <code>Posted</code> variable.  The result of the script is then encoded to the client, based on the <code>Accept</code> header in the HTTP Request, which should be <code>text/html</code>.</p>
<h3 id="generationOfJavascript" class="tocReference">Generation of JavaScript</h3>
<p>The Markdown engine can generate JavaScript for you automatically, facilitating the dynamic creation of items on web pages. This conversion can be done either by specifying an <code>Accept: application/javascript</code> header when requesting for a Markdown file, or by referring to a Markdown file with an additional <code>.js</code> extension after the traditional <code>.md</code> extension. Referring this way to a file <code>Test.md.js</code> for instance, will generate a JavaScript rendering of the <code>Test.md</code> file. This method is useful if referring to JavaScript files from the header of an HTML file, for instance, where you cannot control the browser&rsquo;s selection of HTTP Accept header field in the request.</p>
<p>When converting a Markdown file (for example <code>Test.md</code>) to JavaScript (for example <code>Test.md.js</code>), two functions are created and included in the file:</p>
<pre><code class="javascript">function CreateHTMLTest(Args);
function CreateInnerHTMLTest(ElementId, Args);
</code></pre>
<p>The final <code>Test</code> in the funcion names are taken from the name of the Markdown file being converted. This makes it possible to include multiple JavaScript files generated from multiple Markdown files on the same page. The <code>Args</code> argument can be used to send information to the function, which is later used by inline script when generating HTML.</p>
<p>The first function returns a string containing the HTML generated by the JavaScript. The second function calls the first function to generate HTML, the looks in the DOM of the page to find an element with a given <code>id</code> attribute, and then sets the <code>innerHTML</code> property of that element to the generated HTML.</p>
<p>Things to keep in mind when converting Markdown to JavaScript:</p>
<ul>
<li><p>Script placed between double braces <code>{{</code> and <code>}}</code> is preprocessed on the server and affect the structure of the Markdown, which in turn affects the generated JavaScript. Such script do not have access to the <code>Args</code> argument. Instead they have access to any session variables that may exist.</p>
</li>
<li><p>Script placed between single braces <code>{</code> and <code>}</code> is not processed on the server at all. Instead, it is assumed to be JavaScript itself, and inserted as-is into the JavaScript. This allows you to populate the dynamic HTML using values from your browser, without having to request the server to do it. This also means, that the script syntax normally used for single-braces evaluation on the server, is not used in the JavaScript case. The inline script has access to <code>Args</code>, but as it runs in the browser, does not have access to server-side session-state variables.</p>
</li>
<li><p>If the Markdown only contains a header-less table (i.e. a table with zero header rows), the JavaScript rendered will only generate the table rows, not the surrounding <code>table</code>, <code>thead</code> and <code>tbody</code> elements, to facilitate dynamic addition of rows to a table.</p>
</li>
</ul>
<h4 id="generatedJavascriptExample" class="tocReference">Generated JavaScript Example</h4>
<p>Consider the following Markdown page, saved as <code>Test.md</code>:</p>
<pre><code class="nohighlight">JavaScript: TestTable.md.js
Title: JavaScript generation test
Description: This page displays a table dynamically generated by JavaScript, rendered from a Markdown template.
AllowScriptTag: 1

JavaScript generation Test
-----------------------------

The following table was generated by JavaScript:

&lt;div id="TestTableLocation"&gt;&lt;/div&gt;

&lt;script&gt;
CreateInnerHTMLTestTable("TestTableLocation", {"A": 5, "B": 7});
&lt;/script&gt;
</code></pre>
<p>It refers to a Markdown template called <code>TestTable.md</code>, in a JavaScript header. To make sure the server converts this Markdown to JavaScript, the extension <code>.js</code> is added to the filename, resulting in a reference to <code>TestTable.md.js</code> file. When the browser requests this file, the server recognizes that the file does not exist. Instead, it recognizes the <code>.js</code> extension, understands that it refers to the <code>Accept: application/javascript</code> header, and modifies the request to refer to <code>TestTable.md</code> with the corresponding <code>Accept</code> header set. The server then loads the Markdown, converts it to JavaScript, and returns JavaScript that generates HTML from the following Markdown template:</p>
<pre><code class="nohighlight">| Table populated by JavaScript   ||
|:---------------|-----------------|
| A:             | {Args.A}        |
| B:             | {Args.B}        |
| A+B:           | {Args.A+Args.B} |
| A-B:           | {Args.A-Args.B} |
| A\*B:          | {Args.A*Args.B} |
| A/B:           | {Args.A/Args.B} |
</code></pre>
<p>This will generate a page similar to:</p>
<h2 id="javascriptGenerationTest">JavaScript generation Test</h2>
<p>The following table was generated by JavaScript:</p>
<div id="TestTableLocation"><table>
<colgroup>
<col style="text-align:left">
<col style="text-align:left">
</colgroup>
<thead>
<tr>
<th style="text-align:left" colspan="2">Table populated by JavaScript</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">A:</td>
<td style="text-align:left">5</td>
</tr>
<tr>
<td style="text-align:left">B:</td>
<td style="text-align:left">7</td>
</tr>
<tr>
<td style="text-align:left">A+B:</td>
<td style="text-align:left">12</td>
</tr>
<tr>
<td style="text-align:left">A-B:</td>
<td style="text-align:left">-2</td>
</tr>
<tr>
<td style="text-align:left">A*B:</td>
<td style="text-align:left">35</td>
</tr>
<tr>
<td style="text-align:left">A/B:</td>
<td style="text-align:left">0.7142857142857143</td>
</tr>
</tbody>
</table>
</div>
</section>
<section>
<h2 id="metadata" class="tocReference">Metadata</h2>
<p>The first block in a markdown document has the option to be a metadata block. Such a block is not directly visible on the page, but is used to provide metadata information to the parser, search engines and other entities loading the page. Metadata is provided in the following form:</p>
<pre><code class="nohighlight">Key1: Value 1
Key2: Value 2
...
</code></pre>
<p>Apart from providing metadata information about the page, you can access the metadata information from your page by using the <code>[%Key]</code> operator. That operator will be replaced by the value of the korresponding <code>key</code>. Example:</p>
<pre><code class="nohighlight">The title of this document is "[%Title]". It describes [%Description]
It was written [%Date] by [%Author].
</code></pre>
<p>This is then transformed to:</p>
<p>The title of this document is &ldquo;Markdown&rdquo;. It describes Markdown syntax reference, as understood by the TAG Neuron. It was written 2016-02-11 by Peter Waher.</p>
<p>Note: If a metadata record does not exist for a given key, but a variable exists with the given name, the corresponding variable value will be inserted instead.</p>
<p>The following subsections list the different metadata keys that have special meaning to the <strong>TAG Neuron</strong> Markdown parser. You&rsquo;re not limited to  these metadata keys, and can freely add your own.</p>
<h3 id="allowscripttag" class="tocReference">AllowScriptTag</h3>
<p>If the <code>&lt;SCRIPT&gt;</code> tag should be allowed or not. Value is a boolean value. Strings representing <code>true</code>, include <code>1</code>, <code>true</code>, <code>yes</code> and <code>on</code>. Strings representing <code>false</code>, include <code>0</code>, <code>false</code>, <code>no</code> and <code>off</code>.</p>
<p>Default value, if not provided, is <code>false</code>.</p>
<h3 id="alternate" class="tocReference">Alternate</h3>
<p>Link to alternate page.</p>
<h3 id="audioautoplay" class="tocReference">AudioAutoplay</h3>
<p>If audio should be played automatically or not. Value is a boolean value. Strings representing <code>true</code>, include <code>1</code>, <code>true</code>, <code>yes</code> and <code>on</code>. Strings representing <code>false</code>, include <code>0</code>, <code>false</code>, <code>no</code> and <code>off</code>.</p>
<p>Default value, if not provided, is <code>true</code>.</p>
<h3 id="audiocontrols" class="tocReference">AudioControls</h3>
<p>If audio should be played automatically or not. Value is a boolean value. Strings representing <code>true</code>, include <code>1</code>, <code>true</code>, <code>yes</code> and <code>on</code>. Strings representing <code>false</code>, include <code>0</code>, <code>false</code>, <code>no</code> and <code>off</code>.</p>
<p>Default value, if not provided, is <code>false</code>.</p>
<h3 id="author" class="tocReference">Author</h3>
<p>Write the name of the author or authors using this tag.</p>
<h3 id="bodyonly" class="tocReference">BodyOnly</h3>
<p>If only the contents of the body should be returned or not. This is useful if you create dynamic pages using the XmlHttpRequest object (AJAX), as it removes the DOCTYPE and header (and body tag) from the response, and only returns the corresponding HTML content. Value is a boolean  value. Strings representing <code>true</code>, include <code>1</code>, <code>true</code>, <code>yes</code> and <code>on</code>. Strings representing <code>false</code>, include <code>0</code>, <code>false</code>, <code>no</code> and <code>off</code>.</p>
<p>Default value, if not provided, is <code>false</code>.</p>
<h3 id="copyright" class="tocReference">Copyright</h3>
<p>Allows you to provide a link to a copyright statement.</p>
<h3 id="css" class="tocReference">CSS</h3>
<p>Links to Cascading Style Sheets that should be used for visual formatting of the generated HTML page.</p>
<h3 id="date" class="tocReference">Date</h3>
<p>Provide a date for when the document was created. This date is presented in the metadata header of the document. The web server uses the last write date of the file to tell clients when the file was last updated.</p>
<h3 id="description" class="tocReference">Description</h3>
<p>Provides a description for the page. This description is shown to search engines and other clients, and should contain a short description of the page motivating people to view your page.</p>
<h3 id="details" class="tocReference">Details</h3>
<p>Points to the place in a master document, where the details section is to be inserted. The <code>[%Details]</code> operator differs from the other meta reference tags, in that it can stand alone in a separate block.</p>
<h3 id="help" class="tocReference">Help</h3>
<p>Link to help page.</p>
<h3 id="icon" class="tocReference">Icon</h3>
<p>Link to an icon for the page.</p>
<h3 id="image" class="tocReference">Image</h3>
<p>Link to an image for the page.</p>
<h3 id="init" class="tocReference">Init</h3>
<p>Links to server-side script files that should be executed before processing the page. The script is only executed once, regardless of how many times the markdown page is processed. It can be used to initialize the backend appropriately. To execute the script again, a newer version must be available. The file time stamps are used to determine if a file is newer than a previous version or not. For script that  is to be executed every time the page is processed, see the <a href="#script">Script</a> tag.</p>
<h3 id="javascript" class="tocReference">JavaScript</h3>
<p>Links to JavaScript files that should be included in the generated HTML page.</p>
<h3 id="keywords" class="tocReference">Keywords</h3>
<p>Here you can provide a set of keywords describing the contents of the document.</p>
<h3 id="login" class="tocReference">Login</h3>
<p>Link to a login page. This page will be shown if the user variable does not contain a valid user.</p>
<h3 id="master" class="tocReference">Master</h3>
<p>Points to a master content file that embeds the current file in a <code>[%Details]</code> section (if written in Markdown).</p>
<h3 id="next" class="tocReference">Next</h3>
<p>Link to next document, in a paginated set of documents.</p>
<h3 id="parameter" class="tocReference">Parameter</h3>
<p>Name of a query parameter recognized by the page. Any query parameter values for parameters listed in the document will be available in script. If the query parameters are missing, the corresponding parameters will be set to empty strings. By default, all parameters are strings, unless they can be parsed as a double number or boolean value.</p>
<h3 id="previousOrPrev" class="tocReference">Previous or Prev</h3>
<p>Link to previous document, in a paginated set of documents.</p>
<h3 id="privilege" class="tocReference">Privilege</h3>
<p>Requered user privileges to display page. Meta-data tag can be used multiple times, one for each privilege required. The <code>IUser.HasPrivilege</code> method (defined in <code>Waher.Security</code>) will be called to check that the valid user has the corresponding privilege,  before the page is displayed.</p>
<h3 id="refresh" class="tocReference">Refresh</h3>
<p>Tells the browser to refresh the page after a given number of seconds.</p>
<h3 id="script" class="tocReference">Script</h3>
<p>Links to server-side script files that should be included before processing the page. Script linked to here will be executed every time the markdown document is processed. For script that is to be executed only once, see the <a href="#init">Init</a> tag.</p>
<h3 id="subtitle" class="tocReference">Subtitle</h3>
<p>Provides a means to create a subtitle for the document. If provided, will be shown, together with the title, in the browser header or tab.</p>
<h3 id="title" class="tocReference">Title</h3>
<p>Use this key to provide a title for the document. The title of the page will be shown in the browser header or tab.</p>
<h3 id="uservariable" class="tocReference">UserVariable</h3>
<p>Name of the variable that will hold a reference to the user object for the currently logged in user. If privileges are defined using the  <a href="#privilege">Privilege</a> meta-data tag, this user object must implement the <code>IUser</code> interface (defined in <code>Waher.Security</code>). If multiple UserVariable meta-data tags are defined, the first one that is found will be used.</p>
<h3 id="videoautoplay" class="tocReference">VideoAutoplay</h3>
<p>If video should be played automatically or not. Value is a boolean value. Strings representing <code>true</code>, include <code>1</code>, <code>true</code>, <code>yes</code> and <code>on</code>. Strings representing <code>false</code>, include <code>0</code>, <code>false</code>, <code>no</code> and <code>off</code>.</p>
<p>Default value, if not provided, is <code>false</code>.</p>
<h3 id="videocontrols" class="tocReference">VideoControls</h3>
<p>If video should be played automatically or not. Value is a boolean value. Strings representing <code>true</code>, include <code>1</code>, <code>true</code>, <code>yes</code> and <code>on</code>. Strings representing <code>false</code>, include <code>0</code>, <code>false</code>, <code>no</code> and <code>off</code>.</p>
<p>Default value, if not provided, is <code>true</code>.</p>
<h3 id="viewport" class="tocReference">Viewport</h3>
<p>Defines Viewport meta-data for the page, for better presentation on mobile-phones and devices. See <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Viewport_meta_tag" target="_blank">Using the viewport meta tag to control layout on mobile browsers</a>  for more information.</p>
<h3 id="web" class="tocReference">Web</h3>
<p>Link to a web page.</p>
<h2 id="httpHeaderFields" class="tocReference">HTTP Header Fields</h2>
<p>The following meta-data tags are transparently mapped to HTTP response headers when the markdown document is converted to HTML over a web interface.</p>
<h3 id="accessControlAllowOrigin" class="tocReference">Access-Control-Allow-Origin</h3>
<p>Allows you to define a <a href="http://www.w3.org/TR/cors/" target="_blank">Cross-origin resource sharing (CORS)</a> header.</p>
<h3 id="cacheControl" class="tocReference">Cache-Control</h3>
<p>The value of this tag will be used when returning the document over an HTTP interface. The value will be literally used as a <code>Cache-control</code> HTTP header value of the generated HTML contents. Together with the <a href="#vary">Vary</a> meta-tag they provide a means to control how the generated page will be cached.</p>
<p><strong>Note</strong>: If the markdown page is dynamic, and no <code>Cache-Control</code> metadata header is present, the following HTTP header will be added automatically:</p>
<pre><code class="nohighlight">Cache-Control: max-age=0, no-cache, no-store
</code></pre>
<p>If the markdown page is static, and no <code>Cache-Control</code> tag is present, the following will be used:</p>
<pre><code class="nohighlight">Cache-Control: no-transform,public,max-age=60,s-maxage=60,stale-while-revalidate=604800
</code></pre>
<h3 id="contentSecurityPolicy" class="tocReference">Content-Security-Policy</h3>
<p>Allows web clients to know what the expected behaviour of the page is, by setting <a href="http://www.w3.org/TR/CSP/" target="_blank">Content Security Policies</a>.</p>
<h3 id="publicKeyPins" class="tocReference">Public-Key-Pins</h3>
<p>Tells web clients to <a href="https://tools.ietf.org/html/rfc7469" target="_blank">pin a specific public key</a> with the site, to decrease the risk of MITM attacks.</p>
<h3 id="strictTransportSecurity" class="tocReference">Strict-Transport-Security</h3>
<p><a href="https://tools.ietf.org/html/rfc6797" target="_blank">HTTP Strict Transport Security (HSTS)</a> forces clients to connect to the site using a secure connection.</p>
<h3 id="sunset" class="tocReference">Sunset</h3>
<p><a href="https://tools.ietf.org/html/draft-wilde-sunset-header" target="_blank">HTTP Sunset Header</a> allows you to flag content for removal at a future point in time. It allows clients to prepare.</p>
<h3 id="vary" class="tocReference">Vary</h3>
<p>The value of this tag will be used when returning the document over an HTTP interface. The value will be literally used as a <code>Vary</code> HTTP header value of the generated HTML contents. Together with the <a href="#cacheControl">Cache-Control</a> meta-tag they provide a means to  control how the generated page will be cached.</p>
</section>
<div class="footnotes">
<hr />
<ol>
<li id="fn-1"><p>With <strong>we</strong>, <em>we</em> mean second-person plural<a href="#fnref-1" class="footnote-backref">&#8617;</a></p>
</li>
<li id="fn-2"><p>With <strong>we</strong>, <em>we</em> mean second-person plural<a href="#fnref-2" class="footnote-backref">&#8617;</a></p>
</li>
<li id="fn-3"><p>This example uses video from <a href="http://techslides.com/sample-webm-ogg-and-mp4-video-files-for-html5" target="_blank">http://techslides.com/sample-webm-ogg-and-mp4-video-files-for-html5</a><a href="#fnref-3" class="footnote-backref">&#8617;</a></p>
</li>
<li id="fn-4"><p>This example uses sound from <a href="http://soundbible.com/2084-Glass-Ping.html" target="_blank">http://soundbible.com/2084-Glass-Ping.html</a><a href="#fnref-4" class="footnote-backref">&#8617;</a></p>
</li>
</ol>
</div>
</main>
<div id ="native-popup-container"></div>
</body>
</html>