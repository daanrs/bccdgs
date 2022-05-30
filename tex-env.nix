# Generated with tex2nix 0.0.0
{ texlive, extraTexPackages ? {} }:
(texlive.combine ({
    inherit (texlive) scheme-small;
    "translator" = texlive."translator";
    "fp" = texlive."fp";
    "xkeyval" = texlive."xkeyval";
    "kvsetkeys" = texlive."kvsetkeys";
    "listings" = texlive."listings";
    "rerunfilecheck" = texlive."rerunfilecheck";
    "ltxcmds" = texlive."ltxcmds";
    "logreq" = texlive."logreq";
    "graphics" = texlive."graphics";
    "auxhook" = texlive."auxhook";
    "uniquecounter" = texlive."uniquecounter";
    "intcalc" = texlive."intcalc";
    "hyperref" = texlive."hyperref";
    "pgf" = texlive."pgf";
    "xcolor" = texlive."xcolor";
    "atbegshi" = texlive."atbegshi";
    "infwarerr" = texlive."infwarerr";
    "todonotes" = texlive."todonotes";
    "amsfonts" = texlive."amsfonts";
    "xypic" = texlive."xypic";
    "etexcmds" = texlive."etexcmds";
    "url" = texlive."url";
    "biblatex" = texlive."biblatex";
    "etoolbox" = texlive."etoolbox";
    "kvdefinekeys" = texlive."kvdefinekeys";
    "iftex" = texlive."iftex";
    "hopatch" = texlive."hopatch";
    "gettitlestring" = texlive."gettitlestring";
    "atveryend" = texlive."atveryend";
    "refcount" = texlive."refcount";
    "kvoptions" = texlive."kvoptions";
    "bitset" = texlive."bitset";
    "minitoc" = texlive."minitoc";
    "letltxmacro" = texlive."letltxmacro";
    "geometry" = texlive."geometry";
    "pdfescape" = texlive."pdfescape";
    "beamer" = texlive."beamer";
    "amsmath" = texlive."amsmath";
    "hycolor" = texlive."hycolor";
    "pdftexcmds" = texlive."pdftexcmds";

} // extraTexPackages))
