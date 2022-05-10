# Generated with tex2nix 0.0.0
{ texlive, extraTexPackages ? {} }:
(texlive.combine ({
    inherit (texlive) scheme-small;
    "fancyvrb" = texlive."fancyvrb";
    "xcolor" = texlive."xcolor";
    "iftex" = texlive."iftex";
    "amsmath" = texlive."amsmath";

} // extraTexPackages))
