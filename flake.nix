{
  description = "bccdgs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        rucausal = pkgs.rPackages.buildRPackage {
          name = "rucausal";
          src = fetchGit {
            url = "https://gitlab.science.ru.nl/gbucur/RUcausal.git";
            ref = "master";
            rev = "866e76075fe946b768ad07d3de2a78f8b86d76e2";
          };
          propagatedBuildInputs = with pkgs.rPackages; [
            Matrix
            Rcpp
            RcppArmadillo
            Rdpack
            stringr
          ];
        };

        rDepends = with pkgs.rPackages; [
          rucausal
          pcalg
          purrr
        ];

        bccdgs_r = pkgs.rPackages.buildRPackage {
          name = "bccdgsr";
          src = ./bccdgsr;
          propagatedBuildInputs = [ rDepends ];
        };

        rEnv = pkgs.rWrapper.override {
          packages = with pkgs.rPackages; [
            rDepends
            devtools
            bccdgs_r
          ];
        };

        python39Packages = pkgs.python39Packages.override {
          overrides = self: super: {

            rpy2 = super.rpy2.overridePythonAttrs (
              old: {
                buildInputs = (old.buildInputs or [ ]) ++ (
                  with pkgs.rPackages; [
                    bccdgs_r
                ]);
              }
            );
          };
        };

        myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          overrides = pkgs.poetry2nix.overrides.withDefaults (
            self: super: {
              threadpoolctl = super.threadpoolctl.overridePythonAttrs (
                old: {
                  format = "flit";
                }
              );
            }
          );
        };

        app = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };

        packageName = "bccdgs";
      in
      {
        packages.${packageName} = app;

        defaultPackage = self.packages.${system}.${packageName};

        devShell = myAppEnv.env.overrideAttrs (oldAttrs: {
          buildInputs = with pkgs; [
            poetry
            python39Packages.jupyterlab
            python39Packages.rpy2

            rEnv
          ];
        });
      });
}
