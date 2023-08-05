from edc_visit_schedule import FormsCollection, Crf

crfs_prn = FormsCollection(
    Crf(show_order=10, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=20, model="meta_subject.bloodresultsglu"),
    Crf(show_order=30, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=40, model="meta_subject.bloodresultslft"),
    Crf(show_order=50, model="meta_subject.bloodresultsrft"),
    Crf(show_order=60, model="meta_subject.urinedipsticktest"),
    name="prn",
)

crfs_unscheduled = FormsCollection(
    Crf(show_order=10, model="meta_subject.bloodresultsglu"),
    Crf(show_order=20, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=30, model="meta_subject.bloodresultslft"),
    Crf(show_order=40, model="meta_subject.bloodresultsrft"),
    Crf(show_order=50, model="meta_subject.malariarapidtest"),
    Crf(show_order=60, model="meta_subject.urinedipsticktest"),
    name="unscheduled",
)


crfs_d1 = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.healtheconomics"),
    Crf(show_order=30, model="meta_subject.medicationadherence"),
    Crf(show_order=40, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=50, model="meta_subject.bloodresultsglu"),
    Crf(show_order=60, model='meta_subject.bloodresultshba1c'),
    Crf(show_order=70, model="meta_subject.bloodresultslft"),
    Crf(show_order=80, model="meta_subject.bloodresultsrft"),
    Crf(show_order=90, model="meta_subject.urinedipsticktest"),
    name="day1",
)

crfs_w2 = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.medicationadherence"),
    name="week2",
)

crfs_1m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.medicationadherence"),
    name="1m",
)

crfs_3m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.medicationadherence"),
    Crf(show_order=30, model="meta_subject.bloodresultslft"),
    Crf(show_order=40, model="meta_subject.bloodresultsrft"),
    name="3m",
)

crfs_6m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.medicationadherence"),
    Crf(show_order=30, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=40, model="meta_subject.bloodresultslft"),
    Crf(show_order=50, model="meta_subject.bloodresultsrft"),
    name="6m",
)

crfs_9m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.medicationadherence"),
    Crf(show_order=30, model="meta_subject.bloodresultslft"),
    Crf(show_order=40, model="meta_subject.bloodresultsrft"),
    name="9m",
)

crfs_12m = FormsCollection(
    Crf(show_order=10, model="meta_subject.followupvitals"),
    Crf(show_order=15, model="meta_subject.followup"),
    Crf(show_order=20, model="meta_subject.medicationadherence"),
    Crf(show_order=30, model="meta_subject.bloodresultsglu"),
    Crf(show_order=40, model="meta_subject.bloodresultshba1c"),
    Crf(show_order=50, model="meta_subject.bloodresultsfbc"),
    Crf(show_order=60, model="meta_subject.bloodresultslft"),
    Crf(show_order=70, model="meta_subject.bloodresultsrft"),
    Crf(show_order=80, model="meta_subject.urinedipsticktest"),
    name="12m",
)
