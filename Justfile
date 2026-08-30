set dotenv-load := false

audit_dir := justfile_directory() / "deck-list-audit"

doctor:
    just --justfile "{{audit_dir}}/Justfile" doctor

check:
    just --justfile "{{audit_dir}}/Justfile" check

check-current:
    just --justfile "{{audit_dir}}/Justfile" check-current

audit:
    just --justfile "{{audit_dir}}/Justfile" audit

report:
    just --justfile "{{audit_dir}}/Justfile" report

test:
    just --justfile "{{audit_dir}}/Justfile" test

lint:
    just --justfile "{{audit_dir}}/Justfile" lint

verify:
    just --justfile "{{audit_dir}}/Justfile" verify

refresh-oracle:
    just --justfile "{{audit_dir}}/Justfile" refresh-oracle

apply-change PLAN:
    just --justfile "{{audit_dir}}/Justfile" apply-change "{{PLAN}}"
