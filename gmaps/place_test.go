package gmaps

import (
	"encoding/json"
	"errors"
	"testing"

	"github.com/playwright-community/playwright-go"
	"github.com/stretchr/testify/require"
)

type mockPage struct {
	playwright.Page
	evaluateResult any
	evaluateErr    error
}

func (m *mockPage) Evaluate(expression string, arg ...interface{}) (interface{}, error) {
	if m.evaluateErr != nil {
		return nil, m.evaluateErr
	}

	return m.evaluateResult, nil
}

func TestPlaceJobExtractJSON(t *testing.T) {
	t.Parallel()

	t.Run("returns error on nil result", func(t *testing.T) {
		t.Parallel()

		job := &PlaceJob{}
		page := &mockPage{evaluateResult: nil}

		raw, err := job.extractJSON(page)

		require.Error(t, err)
		require.Nil(t, raw)
	})

	t.Run("returns marshaled map", func(t *testing.T) {
		t.Parallel()

		job := &PlaceJob{}
		page := &mockPage{evaluateResult: map[string]any{"foo": "bar"}}

		raw, err := job.extractJSON(page)

		require.NoError(t, err)
		require.JSONEq(t, `{"foo":"bar"}`, string(raw))
	})

	t.Run("trims xssi prefix from string", func(t *testing.T) {
		t.Parallel()

		job := &PlaceJob{}
		page := &mockPage{evaluateResult: ")]}'\n{\"foo\":\"bar\"}"}

		raw, err := job.extractJSON(page)

		require.NoError(t, err)
		require.Equal(t, `{"foo":"bar"}`, string(raw))
	})

	t.Run("propagates evaluation error", func(t *testing.T) {
		t.Parallel()

		job := &PlaceJob{}
		page := &mockPage{evaluateErr: errors.New("boom")}

		raw, err := job.extractJSON(page)

		require.Error(t, err)
		require.Nil(t, raw)
	})
}

func TestNormalizeJSONMeta(t *testing.T) {
	t.Parallel()

	t.Run("handles multiple meta formats", func(t *testing.T) {
		t.Parallel()

		cases := []struct {
			name    string
			input   any
			want    []byte
			wantErr string
		}{
			{
				name:  "bytes",
				input: []byte(`{"foo":"bar"}`),
				want:  []byte(`{"foo":"bar"}`),
			},
			{
				name:  "string",
				input: ")]}'\n{\"foo\":\"bar\"}",
				want:  []byte(`{"foo":"bar"}`),
			},
			{
				name:  "raw message",
				input: json.RawMessage(`{"foo":"bar"}`),
				want:  []byte(`{"foo":"bar"}`),
			},
			{
				name:  "map",
				input: map[string]any{"foo": "bar"},
				want:  []byte(`{"foo":"bar"}`),
			},
			{
				name:    "nil",
				input:   nil,
				wantErr: "missing",
			},
		}

		for _, tc := range cases {
			tc := tc

			t.Run(tc.name, func(t *testing.T) {
				t.Parallel()

				got, err := normalizeJSONMeta(tc.input)
				if tc.wantErr != "" {
					require.ErrorContains(t, err, tc.wantErr)

					return
				}

				require.NoError(t, err)
				require.Equal(t, tc.want, got)
			})
		}
	})
}