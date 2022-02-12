{
  description = "Thesis";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";

    rucausal.url = "/home/daan/code/uni/thesis/bccd";
  };

  outputs = { self, nixpkgs, flake-utils, rucausal }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        rEnv = pkgs.rWrapper.override {
          packages = with pkgs.rPackages; [
            rucausal.defaultPackage.${system}
            Matrix
            Rcpp
            RcppArmadillo
            Rdpack
            stringr

            pcalg
          ];
        };

        myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
        };

        app = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };

        packageName = "thesis";
      in
      {
        packages.${packageName} = app;

        defaultPackage = self.packages.${system}.${packageName};

        devShell = myAppEnv.env.overrideAttrs (oldAttrs: {
          buildInputs = with pkgs; [
            poetry
            python39Packages.jupyterlab

            rEnv
          ];
        });
      });
}
