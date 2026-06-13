# La Quebrada Viva — common commands.
# Run `make help` for the target list.

SHELL := /usr/bin/env bash

VARIANT ?= A
CAM ?= hero
ASSET ?= cob_walls

.PHONY: help smoke preview final finals sub audit lint test pdf boq deck

help:
	@echo "La Quebrada Viva — make targets"
	@echo ""
	@echo "  make smoke                      Build full scene without rendering + ten_rules_check"
	@echo "  make preview VARIANT=A CAM=hero 1280x720 / 128 samples preview -> renders/_preview_<V>_<cam>.png"
	@echo "  make final   VARIANT=A CAM=hero Deliverable final (hero=2560x1440/512, others=1920x1080/256)"
	@echo "  make finals                     Render all 18 finals (A/B/C x 6 cams). Long-running."
	@echo "  make sub     ASSET=cob_walls    Sub-render one asset -> subrenders/<asset>.png"
	@echo "  make audit                      Static audits: ruff + pytest + random_audit + material_audit"
	@echo "  make lint                       ruff check ."
	@echo "  make test                       pytest tests/"
	@echo "  make pdf                        Build Wesley one-pager PDF -> docs/wesley_brief_onepager.pdf"
	@echo "  make boq                        Bill-of-quantities rollup -> docs/boq/boq_rollup.{csv,md}"
	@echo "  make deck                       Escritura signing deck PDF -> docs/escritura_deck/escritura_deck_v1.pdf"
	@echo ""
	@echo "Variables: VARIANT (A|B|C), CAM (hero|stream_up|terrace|cliff|dusk|petal_macro),"
	@echo "           ASSET (any module under lqv/subscene/, minus .py)"

smoke:
	scripts/smoke_test.sh

preview:
	scripts/render_preview.sh $(VARIANT) $(CAM)

final:
	scripts/render_final.sh $(VARIANT) $(CAM)

finals:
	scripts/render_all_finals.sh

sub:
	blender --background --python lqv/subscene/$(ASSET).py

lint:
	ruff check .

test:
	pytest tests/ -v

audit: lint test
	python3 -m lqv.util.random_audit
	python3 -m lqv.util.material_audit run_static

pdf:
	python3 scripts/build_wesley_onepager_pdf.py

boq:
	python3 scripts/build_boq.py

deck: boq
	python3 scripts/build_escritura_deck.py
