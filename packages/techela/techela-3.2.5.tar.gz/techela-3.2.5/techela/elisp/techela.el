;;; techela.el --- techela utilities

;; These need to be defined in .dir-locals.el

;; techela-course-label - a string that is a label
;; techela-course-root - a string to the absolute path of the course root
;;; Commentary:
;;

;;; Code:

(use-package ox-ipynb
  :load-path (lambda () (expand-file-name "ox-ipynb" scimax-dir)))

(use-package json)


(defun techela-load-course-data ()
  "Load course data."
  (let* ((json-object-type 'alist)
	 (json-array-type 'list)
	 (data (json-read-file (expand-file-name "course-data.json" techela-course-root))))

    (setq techela-admin-box-path (expand-file-name (cdr (assoc 'admin-box-path data)))
	  techela-categories (first (cdr (assoc 'categories data)))
	  techela-graders (cdr (assoc 'admin-names data))
	  techela-rubrics (cdr (assoc 'rubrics data)))))



(defun techela-assign ()
  "Export the current heading to an ipynb.
The ipynb will be named with the label corresponding to the
heading you are in.

If you tag an sections with noexport or solution then it will be excluded."
  (interactive)
  (techela-load-course-data)
  (save-restriction
    (org-narrow-to-subtree)
    (unless (org-entry-get nil "LABEL")
      (org-entry-put nil "LABEL" (completing-read "Label: " (org-map-entries
							     (lambda ()
							       (org-entry-get nil "LABEL"))))))
    (unless (org-entry-get nil "POINTS")
      (org-entry-put nil "POINTS" (read-string "Points: ")))

    (unless (org-entry-get nil "TYPE")
      (org-entry-put nil "TYPE" (completing-read "Type: " techela-categories)))

    (unless (org-entry-get nil "RUBRIC")
      (let ((rubric-name (completing-read "Rubric: " (mapcar 'car techela-rubrics))))
	(org-entry-put nil "RUBRIC" rubric-name)
	(org-entry-put nil "RUBRIC_CATEGORIES"
		       (s-join ", " (first (cdr (assoc (intern-soft rubric-name) techela-rubrics)))))
	(org-entry-put nil "RUBRIC_WEIGHTS"
		       (s-join ", " (mapcar 'number-to-string
					    (second (cdr (assoc (intern-soft rubric-name) techela-rubrics))))))))

    (unless (org-entry-get nil "DUEDATE")
      (org-entry-put nil "DUEDATE" (concat (org-read-date t nil nil nil nil) " 23:59:59")))

    (unless (org-entry-get nil "GRADER")
      (org-entry-put nil "GRADER" (completing-read "Grader: " techela-graders)))

    (let* ((original-buffer (current-buffer))
	   (label (or (org-entry-get nil "LABEL")
		      (read-string "Label: ")))
	   (points (org-entry-get nil "POINTS"))
	   (duedate (org-entry-get nil "DUEDATE"))
	   (type (org-entry-get nil "TYPE"))
	   (rubric (org-entry-get nil "RUBRIC"))
	   (rubric-categories (org-entry-get nil "RUBRIC_CATEGORIES"))
	   (rubric-weights (org-entry-get nil "RUBRIC_WEIGHTS"))
	   (body (save-excursion
		   (org-end-of-meta-data t)
		   (buffer-substring (point) (point-max))))
	   (grader (org-entry-get nil "GRADER"))
	   (org-file (expand-file-name (concat label ".org")
				       (expand-file-name "assignments" techela-course-root)))
	   (ipynb (concat label ".ipynb"))
	   (content (s-format "#+OX-IPYNB-KEYWORD-METADATA: assignment points category rubric rubric_categories rubric_weights duedate grader
#+ASSIGNMENT: ${label}
#+POINTS: ${points}
#+DUEDATE: ${duedate}
#+CATEGORY: ${type}
#+RUBRIC: ${rubric}
#+RUBRIC_CATEGORIES: ${rubric-categories}
#+RUBRIC_WEIGHTS: ${rubric-weights}
#+GRADER: ${grader}

${body}" 'aget (list (cons "label" label)
		     (cons "points" points)
		     (cons "duedate" duedate)
		     (cons "type" type)
		     (cons "rubric" rubric)
		     (cons "rubric-categories" rubric-categories)
		     (cons "rubric-weights" rubric-weights)
		     (cons "body" body)
		     (cons "grader" grader)))))

      (org-entry-put nil "DUEDATE" duedate)
      (org-todo nil)

      (with-temp-file org-file
	(insert content))
      (with-current-buffer (find-file org-file)
	(let ((org-export-exclude-tags '("noexport" "solution"))
	      (org-export-with-author nil)
	      (org-export-with-title nil)
	      (export-file-name ipynb))
	  (org-org-export-as-org)
	  (setf (buffer-string)
	  	(with-current-buffer "*Org ORG Export*"
	  	  (buffer-string)))
	  (ox-ipynb-export-to-ipynb-file-and-open)
	  (kill-buffer "*Org ORG Export*")))
      (org-todo "ASSIGNED")
      (kill-buffer (find-buffer-visiting org-file))
      (delete-file org-file))))


(defun techela-admin-solution ()
  "Make a solution ipynb in `techela-admin-box-path' from the current heading.
You have to copy this file to the course github repo when you are
ready to release it."
  (interactive)
  (save-restriction
    (org-narrow-to-subtree)

    (let* ((label (or (org-entry-get nil "LABEL")
		      (read-string "Label: ")))
	   (points (org-entry-get nil "POINTS"))
	   (duedate (org-entry-get nil "DUEDATE"))
	   (type (org-entry-get nil "TYPE"))
	   (rubric (org-entry-get nil "RUBRIC"))
	   (body (progn
		   (org-end-of-meta-data t)
		   (buffer-substring (point) (point-max))))
	   ;; (org-file (concat  techela-admin-box-path "/solutions/" label ".org"))
	   (temporary-file-directory default-directory)
	   (org-file (make-temp-file "tq-solution-" nil ".org"))
	   (ipynb (concat  techela-admin-box-path "/solutions/" label ".ipynb"))
	   (content (s-format "#+ASSIGNMENT: ${label}
#+POINTS: ${points}
#+DUEDATE: ${duedate}
#+CATEGORY: ${type}
#+RUBRIC: ${rubric}

${body}" 'aget (list (cons "label" label)
		     (cons "points" points)
		     (cons "duedate" duedate)
		     (cons "type" type)
		     (cons "rubric" rubric)
		     (cons "body" body)))))

      (org-entry-put nil "DUEDATE" duedate)

      (with-temp-file org-file
	(insert content))

      (with-current-buffer (find-file-noselect org-file)
	(let ((export-file-name ipynb)
	      (org-export-exclude-tags '("noexport")))
	  (ox-ipynb-export-to-ipynb-file-and-open)))

      (delete-file org-file))))

(provide 'techela)

;;; techela.el ends here
