""" Build index from directory listing

index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Begin Jekyll SEO tag v2.5.0 -->
    <title>Seerah Timeline | Seerah-Timeline</title>
    <meta name="generator" content="Jekyll v3.8.5" />
    <meta property="og:title" content="Timeline" />
    <meta property="og:locale" content="en_US" />
    <link rel="canonical" href="https://munawwir.github.io/timeline/" />
    <meta property="og:url" content="https://munawwir.github.io/timeline/" />
    <meta property="og:site_name" content="Munawwir-Seerah-timeline" />
    <script type="application/ld+json">
    {"@type":"WebSite","headline":"Seerah Timeline","url":"https://munawwir.github.io/timeline/","name":"Munawwir-Seerah-timeline","@context":"http://schema.org"}</script>
    <!-- End Jekyll SEO tag -->

    <link rel="stylesheet" href="/timeline/assets/css/style.css?v=d809c76e2f6e766a03e843906627c6d32ceb6981">
  </head>
  <body>
    <div class="wrapper">
      <header>
        <h1><a href="https://munawwir.github.io/timeline/">Seerah Timeline</a></h1>

        <p></p>

        <p class="view"><a href="https://github.com/munawwir/timeline">View the Project on GitHub <small>munawwir/timeline</small></a></p>

        <!-- Insert all page links here -->

        <p class="view">Biographies</p>

        <p class="view"><a href="../bio"><i>&mdash;All Biographies</i></a></p>

        <p class="view">Events</p>

        <p class="view"><a href="../events"><i>&mdash;All Biographies</i></a></p>

      </header>
      <section>
        <h1 id="Seerah-Timeline">Seerah Timeline</h1>
        <h4><a href="https://github.com/munawwir">Yoyo</a> at Darussalam<br>Chicago</h4>

        <p></br></p>

        <!-- Insert main content here -->

        <h2>${header}</h2>

        <p>
          % for i in range(len(names)):
            <a href="${links[i]}">${names[i]}</a><br>
          % endfor
        </p>

        <p>
          Email <a href="mailto:yoyomunawwar@gmail.com">yoyomunawwar@gmail.com</a>.
        </p>

      </section>
      <footer>

        <p><small>This site is maintained by <a href="https://github.com/munawwir">Yoyo</a></small></p>

      </footer>
    </div>
    <script src="/timeline/assets/js/scale.fix.js"></script>

 </body>
</html>
"""

import os
import glob
import argparse
from itertools import chain
from dateutil.parser import parse
# May need to do "pip install mako"
from mako.template import Template


def main():

    def get_html_title(file):
        with open(file, "r", errors="ignore") as f:
            for line in f:
                if "</title>" in line:
                    title = (line.split("<title>")[1].split("</title>")[0])
                    break
        return(title)

    def is_date(string, fuzzy=True):
        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    EXCLUDED = ['index.html','.ignore', '.header']

    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header", "--h", help="Provide a string for a custom header for the index. Defaults to the directory name if unused.")
    parser.add_argument("--exclude", "--e", action="store_true", help="Add this flag to add folders and files not to add in created index. File and folder names should be added to a .ignore file with only a newline between names.")
    parser.add_argument("--custom", "--c", action="store_true", help="Add this flag if there are specific custom file names in a .header file.")
    args = parser.parse_args()

    os.chdir(args.directory)

    if args.exclude:
        try:
            f = open(".ignore","r").read()
            to_parse = [i for i in f.split("\n") if i[:1] == "*"]
            f = [i for i in f.split("\n") if i not in to_parse]
            f = list(filter(None, f))
            EXCLUDED += list(chain(f,*[glob.glob(i) for i in to_parse]))
        except FileNotFoundError:
            print("No .ignore file, no files excluded. Use -h to view description.")
            pass

    header = (args.header if args.header else os.path.basename(args.directory))
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED]
    links = [i[:-3] + ".html" if i[-3:] == ".md" else i for i in fnames]    # replace markdown with html links

    if args.custom:
        CUSTOM = open(".header","r").read()
        CUSTOM = [i + " <i>subdir</i>" for i in CUSTOM.split("\n")]
        CUSTOM = dict(zip([i.split("|")[1] for i in CUSTOM], CUSTOM))
        fnames = ["<b>" + CUSTOM[i].split("|")[1] + "</b> " + " ".join(CUSTOM[i].split("|")[2:]) if i in CUSTOM.keys() else i for i in fnames]

    m_fnames = [i for i in fnames if i[-3:] == ".md"]
    m_content = [open(i, "r", errors="ignore").read() for i in m_fnames]
    markdown = dict(zip(m_fnames, ["<b>" + m_content[i].split("\n")[1].split(" ")[1] + "</b> " + " ".join(m_content[i].split("\n")[0].split(" ")[1:]) for i in range(len(m_fnames))]))
    # markdown = dict(zip(m_fnames, ["<b>" + m_content[i].split("\n")[1].split(" ")[1] + "</b> " + " ".join(m_content[i].split("\n")[0].split(" ")[1:]) + " — " + m_content[i].split("\n")[4] for i in range(len(m_fnames))]))

    h_fnames = [i for i in fnames if i[-5:] == ".html"]
    html = dict(zip([i for i in fnames if i[-5:] == ".html"], ["<b>" + i[:-5] + "</b> " + get_html_title(i) for i in fnames if i[-5:] == ".html"]))

    fnames = [markdown[i] if i in markdown.keys() else i for i in fnames]
    fnames = [html[i] if i in html.keys() else i for i in fnames]

    f = open("index.html", "w")
    f.write(Template(INDEX_TEMPLATE).render(names=fnames, header=header, links=links))
    f.close()


if __name__ == '__main__':
    main()
