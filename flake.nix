{
  description = "Mesa Environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [
        "aarch64-darwin"
      ];

      forAllSystems = f:
        nixpkgs.lib.genAttrs systems
          (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            python312
            uv
          ];

          shellHook = ''
            export UV_PYTHON="${pkgs.python312}/bin/python3.12"
            export UV_PYTHON_DOWNLOADS=never
          '';
        };
      });
    };
}
