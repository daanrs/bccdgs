# Generated with tex2nix 0.0.0
{ texlive, extraTexPackages ? {} }:
(texlive.combine ({
    inherit (texlive) scheme-small;
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
    "infwarerr" = texlive."infwarerr";
    "atbegshi" = texlive."atbegshi";
    "todonotes" = texlive."todonotes";
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
    "kvoptions" = texlive."kvoptions";
    "refcount" = texlive."refcount";
    "bitset" = texlive."bitset";
    "minitoc" = texlive."minitoc";
    "letltxmacro" = texlive."letltxmacro";
    "geometry" = texlive."geometry";
    "pdfescape" = texlive."pdfescape";
    "amsmath" = texlive."amsmath";
    "hycolor" = texlive."hycolor";
    "pdftexcmds" = texlive."pdftexcmds";

} // extraTexPackages))
